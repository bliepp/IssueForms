from .base import IssueAPI



class GithubIssueAPI(IssueAPI):
    def __init__(self):
        super().__init__(
            "https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/.github/ISSUE_TEMPLATE/{FILE_NAME}",
            "https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues",
            )
