from dataclasses import dataclass, field
from datetime import date, datetime
from enum import IntEnum
from typing import Any, Dict, List, Optional


@dataclass
class StandardizedUser:
    id: str
    name: Optional[str]
    login: str
    email: Optional[str] = None
    url: Optional[str] = None
    account_id: Optional[str] = None


@dataclass
class StandardizedTeam:
    id: str
    slug: str
    name: str
    description: Optional[str]
    members: list[StandardizedUser]


@dataclass
class StandardizedBranch:
    name: Optional[str]
    sha: Optional[str]
    repo_id: str
    is_default: bool


@dataclass
class StandardizedOrganization:
    id: str
    name: Optional[str]
    login: str
    url: Optional[str]


@dataclass
class StandardizedShortRepository:
    id: str
    name: str
    url: str


@dataclass
class StandardizedRepository:
    id: str
    name: str
    full_name: str
    url: str
    is_fork: bool
    default_branch_name: Optional[str]
    default_branch_sha: Optional[str]
    organization: StandardizedOrganization
    branches: list = field(default_factory=list)
    commits_backpopulated_to: Optional[datetime] = None
    prs_backpopulated_to: Optional[datetime] = None
    full_path: Optional[str] = (
        None  # This is only used by the Gitlab adapter and is ignored during git import
    )

    def short(self):
        # return the short form of Standardized Repository
        return StandardizedShortRepository(id=self.id, name=self.name, url=self.url)


@dataclass
class StandardizedCommit:
    hash: str
    url: str
    message: str
    commit_date: datetime
    author_date: datetime
    author: Optional[StandardizedUser]
    repo: StandardizedShortRepository
    is_merge: bool
    branch_name: Optional[str] = None


@dataclass
class StandardizedPullRequestComment:
    user: Optional[StandardizedUser]
    body: str
    created_at: datetime
    system_generated: Optional[bool] = None


# TODO: This exists in the Jellyfish source code
# and has been copied over. The source code should be
# replaced with this, so we have one "source of truth".
# NOTE: These enum string values are based off of Github,
# we need to normalize all other providers to this
class PullRequestReviewState(IntEnum):
    UNKNOWN = 0
    PENDING = 1
    APPROVED = 2
    COMMENTED = 3
    CHANGES_REQUESTED = 4
    DISMISSED = 5


@dataclass
class StandardizedPullRequestReview:
    user: Optional[StandardizedUser]
    foreign_id: str
    review_state: str


@dataclass
class StandardizedLabel:
    id: int
    name: str
    default: bool
    description: str


@dataclass
class StandardizedFileData:
    status: str
    changes: int
    additions: int
    deletions: int


@dataclass
class StandardizedPullRequest:
    id: Any
    additions: int
    deletions: int
    changed_files: int
    is_closed: bool
    is_merged: bool
    created_at: datetime
    updated_at: datetime
    merge_date: Optional[datetime]
    closed_date: Optional[datetime]
    title: str
    body: str
    url: str
    base_branch: str
    head_branch: str
    author: StandardizedUser
    merged_by: Optional[StandardizedUser]
    commits: List[StandardizedCommit]
    merge_commit: Optional[StandardizedCommit]
    comments: List[StandardizedPullRequestComment]
    approvals: List[StandardizedPullRequestReview]
    base_repo: StandardizedShortRepository
    head_repo: StandardizedShortRepository
    labels: List[StandardizedLabel]
    files: Dict[str, StandardizedFileData]


@dataclass
class StandardizedPullRequestMetadata:
    id: Optional[Any]
    updated_at: datetime
    # API Index place holder, needed if the adapter DOES NOT support PullRequest API Time filtering
    # (git_provider_pr_endpoint_supports_date_filtering)
    api_index: Optional[Any] = None
