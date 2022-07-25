from enum import Enum
from typing import Optional

from appcore.GitUtils.GitUtils import GitUtils


class GitApiConstants(Enum):
    user_info_url: str = "https://api.github.com/user"
    user_repos_url: str = "https://api.github.com/user/repos?per_page=100"
    user_orgs_url: str = "https://api.github.com/user/orgs?per_page=100"
    repo_branches_url_format: str = "https://api.github.com/repos/{username}/{repo_name}/branches?per_page=100"
    branch_commits_url_format: str = "https://api.github.com/repos/{username}/{repo_name}/commits?sha={" \
                                     "branch_sha}&per_page=100 "
    rate_limit_url: str = "https://api.github.com/rate_limit"


class GitApiUtils(GitUtils):
    def __init__(self, access_token=None):
        super().__init__(access_token)

    def get_user_info(self) -> Optional[dict]:
        return self._handle_user_api_call(GitApiConstants.user_info_url.value)

    def get_all_user_orgs(self) -> Optional[list[dict]]:
        return self._handle_user_api_call(GitApiConstants.user_orgs_url.value)

    def get_all_user_repos(self) -> Optional[list[dict]]:
        return self._handle_user_api_call(GitApiConstants.user_repos_url.value)

    def get_all_repo_branches(self, username: str, repo_name: str) -> Optional[list[dict]]:
        return self._handle_user_api_call(GitApiConstants.repo_branches_url_format.value.format(
            username=username,
            repo_name=repo_name,
        ))

    def get_all_commits_for_branch(self, username: str, repo_name: str, branch_sha: str) -> Optional[dict[list]]:
        return self._handle_user_api_call(GitApiConstants.branch_commits_url_format.value.format(
            username=username,
            repo_name=repo_name,
            branch_sha=branch_sha,
        ))

    def check_rate_limit(self) -> Optional[dict]:
        return self._handle_user_api_call(GitApiConstants.rate_limit_url.value)


