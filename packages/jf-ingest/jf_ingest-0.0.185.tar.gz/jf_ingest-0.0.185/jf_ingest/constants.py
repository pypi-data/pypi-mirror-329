class Constants:
    JELLYFISH_USER_AGENT = f'jellyfish/1.0'
    # This is how many bytes are in a MB. This is used when
    # determining how much data to upload to S3 (we generally)
    # batch files by ~50 MBs
    MB_SIZE_IN_BYTES = 1048576
    JIRA_ISSUES_UNCOMPRESSED_FILE_SIZE = 50 * MB_SIZE_IN_BYTES
    # When inserting JiraIssues to our database we cannot handle
    # any issue that is stringified and larger than 255 MBs
    JIRA_ISSUE_SIZE_LIMIT = 255 * MB_SIZE_IN_BYTES
    # 250 is the default largest value we can pull from Jira Server
    # For cloud it's 100, but we have logic to check what Jira
    # limits us to and reduce our batch size to that
    MAX_ISSUE_API_BATCH_SIZE = 250
    # Uses a pull-by-id approach to fetching sprints
    PULL_SPRINTS_BY_ID = 'makara-pull-sprints-by-id-2024Q4'
