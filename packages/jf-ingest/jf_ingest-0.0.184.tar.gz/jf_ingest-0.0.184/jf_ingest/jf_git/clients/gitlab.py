import json
import logging
from datetime import datetime
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

import gitlab
import requests
from gitlab import Gitlab
from gitlab.base import RESTObject
from gitlab.v4.objects import Project, ProjectBranch, ProjectCommit
from gitlab.v4.objects import User as GitlabUser

from jf_ingest.config import GitAuthConfig
from jf_ingest.constants import Constants
from jf_ingest.graphql_utils import GQL_PAGE_INFO_BLOCK
from jf_ingest.jf_git.standardized_models import (
    StandardizedOrganization,
    StandardizedRepository,
)
from jf_ingest.utils import (
    hash_filename,
    parse_gitlab_api_version,
    retry_for_status,
    retry_session,
)

logger = logging.getLogger(__name__)


class GitlabClient:
    # NOTE: We currently have some functions in this class that access GraphQL.
    # When trying to implement that, we ran into some authentication issues and limitations that moved us toward
    #   using the rest client instead.
    # Functions that make use of GraphQL are suffixed with _gql.
    # If we want to keep them, we'd ideally eventually move them to their own subclass of the client.
    GITLAB_GQL_USER_FRAGMENT = "... on User {login, id: databaseId, email, name, url}"
    GITLAB_GQL_USER_NODES = 'id, name, username, webUrl, publicEmail'
    GITLAB_GQL_SHORT_REPO_NODES = 'id, name, webUrl'

    def __init__(self, auth_config: GitAuthConfig, **kwargs):
        """Gitlab Client, used as a wrapper for getting raw data from the API.
        This client will get data mainly from the GraphQL API endpoints, although
        it will use the REST API endpoints for a small amount of functions as well.

        Args:
            auth_config (GitAuthConfig): A valid GitAuthConfiguration object
            kwargs: kwargs are used to pass arguments to the inner Session object, if no session object is provided as part of the GitAuthConfig
        """
        self.company_slug: str = auth_config.company_slug
        self.rest_api_url: Optional[str] = auth_config.base_url
        self.gql_base_url: str = f'{auth_config.base_url}/api/graphql'
        if session := auth_config.session:
            self.session: requests.Session = session
        else:
            self.session = retry_session(**kwargs)
            self.session.headers.update(
                {
                    'Authorization': f'Bearer {auth_config.token}',
                    'Content-Type': 'application/json',
                    'User-Agent': f'{Constants.JELLYFISH_USER_AGENT} ({requests.utils.default_user_agent()})',
                }
            )
        self.session.verify = auth_config.verify
        self.client: Gitlab = Gitlab(url=self.rest_api_url, session=self.session)
        self.compatibility_config = self.get_api_compatibility_config()

    def get_api_version(self) -> str:
        return str(self.client.http_get('/metadata')['version'])

    def get_api_compatibility_config(self) -> Dict:
        """
        Some versions of the api may be missing functionality. This function is designed to help us work around those.

        Returns:
            compatibility_mapping Dict: A collection of keys and values to help the client handle version differences.
        """
        compatibility_config = {'gql_skip_pr_closed_at': False}

        # Get version stripped of any tags or other letters. This should align roughly with semver
        api_version: str = self.get_api_version()

        if api_version:
            major_version = None
            minor_version = None

            try:
                api_version = parse_gitlab_api_version(api_version)
                version_split = api_version.split('.')
                major_version = int(version_split[0])

                if len(version_split) > 1:
                    minor_version = int(version_split[1])
            except ValueError:
                logger.warning(
                    ':WARN: Unable to determine GitLab server version. Enabling all compatability configuration.'
                )

            # API versions prior to 17.4 do not have closedAt available on the mergedRequest. We can still fetch the rest
            # of the data we want via GQL, but that field needs to be populated via the api for customers on older versions.
            if (not major_version or major_version < 17) or (
                major_version == 17 and (not minor_version or minor_version < 4)
            ):
                compatibility_config['gql_skip_pr_closed_at'] = True

        return compatibility_config

    def get_organization_name_full_path_and_url(self, login: str) -> Tuple[str, str, str]:
        """In Jellyfish Land, the JFGithubOrganization is the normalization of Github Organizations,
        AzureDevops Organizations, Bitbucket Projects, and Gitlab Groups. The login field is the unique
        key. For Gitlab Groups, we set the login to the be the Group ID, which is a numeric value.
        The GraphQL Group Queries accept a "fullPath" argument, and NOT the Group ID. If we only have
        the GroupID (set by the login value), then this helper function can be used to translate the
        GroupID to a Full Path.
        NOTE: For performance reasons, we should probably graph the FullPath when we query GraphQL for
        Groups in general, and then cache those values. We should NOT call this function everytime,
        because it could have performance implications

        Args:
            login (str): The JFGithubOrganization login, which is the Group ID in Gitlab land
        Returns:
            name, full_path, url (str, str, str): The name, Full Path, and url for this gitlab Group
        """
        group_url = f'{self.rest_api_url}/api/v4/groups/{login}?with_projects=False'
        response: requests.Response = retry_for_status(self.session.get, url=group_url)
        response.raise_for_status()
        response_json = response.json()
        return (
            str(response_json['name']),
            str(response_json['full_path']),
            str(response_json['web_url']),
        )

    def get_raw_result_gql(self, query_body: str, max_attempts: int = 7) -> Dict:
        """Gets the raw results from a Graphql Query.

        Args:
            query_body (str): A query body to hit GQL with
            max_attempts (int, optional): The number of retries we should make when we specifically run into GQL Rate limiting. This value is important if the GQL endpoint doesn't give us (or gives us a malformed) rate limit header. Defaults to 7.

        Raises:
            GqlRateLimitExceededException: A custom exception if we run into GQL rate limiting and we run out of attempts (based on max_attempts)
            Exception: Any other random exception we encounter, although the big rate limiting use cases are generally covered

        Returns:
            dict: A raw dictionary result from GQL
        """
        response: requests.Response = retry_for_status(
            self.session.post,
            url=self.gql_base_url,
            json={'query': query_body},
            max_retries_for_retry_for_status=max_attempts,
        )
        json_str = response.content.decode()
        json_data: Dict = json.loads(json_str)
        if error_list_dict := json_data.get('errors'):
            error_message = ','.join([error_dict.get('message') for error_dict in error_list_dict])
            raise Exception(
                f'An error occurred when attempting to query GraphQL (response code {response.status_code}): {error_message}'
            )

        return json_data

    def page_results_gql(
        self, query_body: str, path_to_page_info: str, cursor: Optional[str] = None
    ) -> Generator[Dict, None, None]:
        """This is a helper function for paging results from GraphQL. It expects
        a query body to hit Graphql with that has a %s marker after the "after:"
        key word, so that we can inject a cursor into the query. This will allow
        us to page results in GraphQL.
        To use this function properly, the section you are trying to page MUST
        INCLUDE VALID PAGE INFO (including the hasNext and endCursor attributes)

        Args:
            query_body (str): The query body to hit GraphQL with
            path_to_page_info (str): A string of period separated words that lead
            to the part of the query that we are trying to page. Example: data.organization.userQuery
            cursor (str, optional): LEAVE AS NULL - this argument is use recursively to page. The cursor
            will continuously go up, based on the endCursor attribute in the GQL call. Defaults to 'null'.

        Yields:
            Generator[dict, None, None]: This function yields each item from all the pages paged, item by item
        """
        hasNextPage = True
        if not cursor:
            cursor = 'null'
        else:
            cursor = f'"{cursor}"'

        while hasNextPage:
            # Fetch results
            result = self.get_raw_result_gql(query_body=(query_body % cursor))

            yield result

            # Get relevant data and yield it
            path_tokens = path_to_page_info.split('.')
            for token in path_tokens:
                result = result[token]

            page_info = result['pageInfo']
            # Need to grab the cursor and wrap it in quotes
            _cursor = page_info['endCursor']
            # If endCursor returns null (None), break out of loop
            hasNextPage = page_info['hasNextPage'] and _cursor
            cursor = f'"{_cursor}"'

    def get_teams(self, *args, **kwargs) -> list:
        """
        This function is to align with other clients.
        GitLab does not have a concept of teams past groups, which we use as organizations.
        This will return an empty list, regardless of arguments.
        """
        return []

    def get_repos(
        self, jf_org: StandardizedOrganization
    ) -> Generator[Project | RESTObject, None, None]:
        group = self.client.groups.get(jf_org.login)

        for repo in group.projects.list(iterator=True, include_subgroups=True):
            yield repo

    def get_commits(
        self,
        jf_repo: StandardizedRepository,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        branch_name: Optional[str] = None,
    ) -> Generator[ProjectCommit | RESTObject, None, None]:
        project_id = jf_repo.id
        project = self.client.projects.get(project_id)

        kwargs_dict: dict[str, Any] = {
            'iterator': True,  # Returns a generator
        }
        if branch_name:
            kwargs_dict['ref_name'] = branch_name
        if since:
            kwargs_dict['since'] = since
        if until:
            kwargs_dict['until'] = until

        for commit in project.commits.list(**kwargs_dict):
            yield commit

    def get_branches_for_repo(
        self, jf_repo: StandardizedRepository, branch_name: Optional[str] = None
    ) -> Generator[ProjectBranch | RESTObject, None, None]:
        """
        Attempts to pull branches for a given repository.

        Args:
            standardized_repo (StandardizedRepository): A standardized repo, which is used to pull repositories.
            branch_name (Optional[str]): Name of the branch to pull. If this is provided, only attempt to pull this
                branch. Otherwise, attempts to pull all branches.

        Yields:
            ProjectBranch | RESTObject: Objects generated by the GitLab client.
        """
        project_id = jf_repo.id
        project = self.client.projects.get(project_id)
        branches_list: List[ProjectBranch | RESTObject] = []

        kwargs_dict: dict[str, Any] = {'iterator': True}
        if branch_name:
            try:
                branches_list.append(project.branches.get(branch_name))
            except gitlab.exceptions.GitlabGetError:
                try:
                    # Per legacy code (scc 1/9/2023), we may hit this for very old GitLab servers (<11.9).
                    # In this case, we hit the branch list endpoint and use the given branch name as the search term.
                    logger.warning(
                        f"GitLab client error retrieving individual branch '{branch_name}' for '{self.client.api_url}'"
                    )

                    # We technically could use regex here to reduce extra hits, but we're not guaranteed to have regex on
                    # very old versions of GitLab's api. Limit this to 10 per page, likely to have a hit there.
                    kwargs_dict['search'] = branch_name
                    kwargs_dict['per_page'] = 10
                    branches = project.branches.list(**kwargs_dict)

                    # If we're given a branch name, we only expect one branch back. We *may* get more than one, so just
                    # return the first we get that completely matches the branch name.
                    for branch in branches:
                        if branch.name == branch_name:
                            branches_list.append(branch)
                            break

                except gitlab.exceptions.GitlabListError:
                    # We believe Gitlab does this to mean "0 results".
                    logger.warning(f"No branches found with name '{branch_name}'.")
        else:
            yield from project.branches.list(**kwargs_dict)

        for branch in branches_list:
            yield branch

    def get_organizations_gql(
        self, page_size: int = 100, sort_key: str = 'id_asc'
    ) -> Generator[Dict, None, None]:
        query_body = f"""
        {{
            groupsQuery: groups(first: {page_size}, sort: "{sort_key}", after: %s){{
                {GQL_PAGE_INFO_BLOCK}
                groups: nodes {{
                    groupIdStr: id
                    name
                    fullPath
                    webUrl
                }}
            }}
        }}
        """
        for page in self.page_results_gql(
            query_body=query_body, path_to_page_info='data.groupsQuery'
        ):
            for group in page['data']['groupsQuery']['groups']:
                yield group

    def get_repos_gql(
        self, group_full_path: str, page_size: int = 100
    ) -> Generator[Dict, None, None]:
        query_body = f"""
        {{
            group(fullPath: "{group_full_path}") {{
                projectsQuery: projects(first: {page_size}, after: %s) {{
                    {GQL_PAGE_INFO_BLOCK}
                    projects: nodes {{
                        ... on Project {{
                            name,
                            webUrl,
                            description,
                            isForked,
                            repository {{
                                ... on Repository {{
                                    defaultBranchName: rootRef
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """
        for page in self.page_results_gql(
            query_body=query_body, path_to_page_info='data.group.projectsQuery'
        ):
            for project in page['data']['group']['projectsQuery']['projects']:
                yield project

    def get_users(self, group_id: str) -> Generator[Union[RESTObject, GitlabUser], None, None]:
        """
        Gets all users for a given Gitlab group (aka organization)

        Args:
            group_id: ID of the group (organization) to get users for

        Returns:
            Generator[Union[RESTObject, GitlabUser], None, None]: Generator yielding one user object at a time
        """
        group = self.client.groups.get(group_id)

        for user in group.members.list(all=True, iterator=True):
            yield user

    def get_prs(
        self,
        project_full_path: str,
        start_cursor: Optional[Any] = None,
        start_window: Optional[datetime] = None,
        end_window: Optional[datetime] = None,
        pull_files_for_pr: Optional[bool] = False,
        hash_files_for_pr: Optional[bool] = False,
        page_size: int = 25,
    ) -> Generator[Dict, None, None]:
        """
        Gets all pull requests for a given Gitlab project (aka repository) using GraphQL

        Args:
            project_full_path (str): Full path of the project (repository) to get pull requests for
            start_cursor (Optional[str]): A cursor string to start from when fetching prs, defaults to None
            start_window (Optional[datetime]): Filter prs to those updated after this date. defaults to None
            end_window (Optional[datetime]): Filter prs to those updated before this date. defaults to None
            pull_files_for_pr (Optional[bool]): Used to determine if we should pull file data with prs, defaults to False
            hash_files_for_pr (Optional[bool]): Used to determine if pulled filenames should be hashed, defaults to False
                Only applied to filenames, so will have no effect if pull_files_for_pr is False
            page_size (int): Page size for the API call, defaults to 25

        Returns:
            Generator[Dict, None, None]: Generator yielding one pull request dict at a time
        """
        query_body = f"""
        {{
            project(fullPath: "{project_full_path}") {{
                mergeRequests(first: {page_size}, after: %s, sort: UPDATED_DESC{f', updatedAfter: "{start_window.isoformat()}"' if start_window else ''}{f', updatedBefore: "{end_window.isoformat()}"' if end_window else ''}) {{
                    {GQL_PAGE_INFO_BLOCK}
                    nodes {{
                        id
                        iid
                        {'closedAt' if not self.compatibility_config['gql_skip_pr_closed_at'] else ''},
                        updatedAt
                        mergedAt
                        createdAt
                        title
                        description
                        webUrl
                        sourceBranch
                        targetBranch
                        mergeCommitSha
                        diffStatsSummary {{ additions, deletions, fileCount }}
                        {'diffStats { additions, deletions, path }' if pull_files_for_pr else ''},
                        sourceProject {{ {self.GITLAB_GQL_SHORT_REPO_NODES} }}
                        targetProject {{ {self.GITLAB_GQL_SHORT_REPO_NODES} }}
                        author {{ {self.GITLAB_GQL_USER_NODES} }}
                        mergeUser {{ {self.GITLAB_GQL_USER_NODES} }}
                        {self._get_pr_commits_query_block(enable_paging=False)}
                        {self._get_pr_comments_query_block(enable_paging=False)}
                        {self._get_pr_approvals_query_block(enable_paging=False)}
                    }}
                }}
            }}
        }}
        """

        for page in self.page_results_gql(
            query_body=query_body,
            path_to_page_info='data.project.mergeRequests',
            cursor=start_cursor,
        ):
            for pr_node in page['data']['project']['mergeRequests']['nodes']:
                pr_iid = pr_node['iid']

                # Fetch any commits not fetched on initial page
                if pr_node['commits']['pageInfo']['hasNextPage']:
                    commits = [
                        commit
                        for commit in self.get_pr_commits(
                            project_full_path=project_full_path,
                            pr_iid=pr_iid,
                        )
                    ]
                    pr_node['commits']['nodes'] = commits

                # Fetch any comments not fetched on initial page
                if pr_node['notes']['pageInfo']['hasNextPage']:
                    comments = [
                        comment
                        for comment in self.get_pr_comments(
                            project_full_path=project_full_path,
                            pr_iid=pr_iid,
                        )
                    ]
                    pr_node['notes']['nodes'] = comments

                # Fetch any approvals not fetched on initial page
                if pr_node['approvedBy']['pageInfo']['hasNextPage']:
                    approvals = [
                        approval
                        for approval in self.get_pr_approvals(
                            project_full_path=project_full_path,
                            pr_iid=pr_iid,
                        )
                    ]
                    pr_node['approvedBy']['nodes'] = approvals

                # Hash filenames if enabled and we have file paths to hash
                if pull_files_for_pr and hash_files_for_pr:
                    hashed_files = []
                    for unhashed_file in pr_node['diffStats']:
                        unhashed_file['path'] = hash_filename(unhashed_file['path'])
                        hashed_files.append(unhashed_file)
                    pr_node['diffStats'] = hashed_files

                yield pr_node

    def get_pr_commits(
        self,
        project_full_path: str,
        pr_iid: str,
    ) -> Generator[dict, None, None]:
        query_body = f"""   
        {{         
            project(fullPath: "{project_full_path}") {{
                mergeRequest(iid: "{pr_iid}") {{
                    {self._get_pr_commits_query_block(enable_paging=True)}
                }}
            }}
        }}
        """
        for page in self.page_results_gql(
            query_body=query_body,
            path_to_page_info='data.project.mergeRequest.commits',
        ):
            for node in page['data']['project']['mergeRequest']['commits']['nodes']:
                yield node

    def get_pr_comments(
        self,
        project_full_path: str,
        pr_iid: str,
    ) -> Generator[dict, None, None]:
        query_body = f"""
        {{      
            project(fullPath: "{project_full_path}") {{
                mergeRequest(iid: "{pr_iid}") {{
                    {self._get_pr_comments_query_block(enable_paging=True)}
                }}
            }}
        }}
        """
        for page in self.page_results_gql(
            query_body=query_body,
            path_to_page_info='data.project.mergeRequest.notes',
        ):
            for node in page['data']['project']['mergeRequest']['notes']['nodes']:
                yield node

    def get_pr_approvals(
        self,
        project_full_path: str,
        pr_iid: str,
    ) -> Generator[dict, None, None]:
        query_body = f"""
        {{       
            project(fullPath: "{project_full_path}") {{
                mergeRequest(iid: "{pr_iid}") {{
                    {self._get_pr_approvals_query_block(enable_paging=True)}
                }}
            }}
        }}
        """
        for page in self.page_results_gql(
            query_body=query_body,
            path_to_page_info='data.project.mergeRequest.approvedBy',
        ):
            for node in page['data']['project']['mergeRequest']['approvedBy']['nodes']:
                yield node

    def _get_pr_commits_query_block(self, enable_paging: bool = False):
        return f"""
            commits(first: 20{', after: %s' if enable_paging else ''}) {{
                {GQL_PAGE_INFO_BLOCK}
                nodes {{
                    id
                    sha
                    webUrl
                    message
                    committedDate
                    authoredDate
                    author {{ {self.GITLAB_GQL_USER_NODES} }}
                }}
            }}
        """

    def _get_pr_comments_query_block(self, enable_paging: bool = False):
        return f"""
            notes(first: 20{', after: %s' if enable_paging else ''}) {{
                {GQL_PAGE_INFO_BLOCK}
                nodes {{
                    id
                    body
                    createdAt
                    system
                    author {{ {self.GITLAB_GQL_USER_NODES} }}
                }}
            }}
        """

    def _get_pr_approvals_query_block(self, enable_paging: bool = False):
        return f"""
            approvedBy(first: 20{', after: %s' if enable_paging else ''}) {{
                {GQL_PAGE_INFO_BLOCK}
                nodes {{ {self.GITLAB_GQL_USER_NODES} }}
            }}
        """
