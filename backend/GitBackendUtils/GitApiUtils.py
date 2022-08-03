from enum import Enum
from typing import Optional, List, Dict
from requests import get as requests_get
from backend.GitBackendUtils.GitApiExceptions import GitApiLimit, GitApiResponseParsingError, GitApiUnknownStatusCode
import logging
from json import loads as json_loads


class GitApiConstants(Enum):
    user_info_url: str = "https://api.github.com/user"
    user_repos_url: str = "https://api.github.com/user/repos?per_page=100"
    user_orgs_url: str = "https://api.github.com/user/orgs?per_page=100"
    repo_branches_url_format: str = "https://api.github.com/repos/{username}/{repo_name}/branches?per_page=100"
    branch_commits_url_format: str = "https://api.github.com/repos/{username}/{repo_name}/commits?sha={" \
                                     "branch_sha}&per_page=100 "
    rate_limit_url: str = "https://api.github.com/rate_limit"


class GitApiUtils:
    def __init__(self, access_token=None):
        self._access_token = access_token
        self._auth_headers = {
            "Authorization": "token " + access_token,
            "Accept": "application/vnd.github.v3+json"
        }

    def _check_user_api_limit(self):
        pass

    def _handle_api_limit(self):
        logging.warning("User API limit reached.")
        raise GitApiLimit  # Missing database sync for storing user timeout
    
    def _handle_user_api_call(self, url: str) -> Optional[Dict]:
        self._check_user_api_limit()
        response = requests_get(
            url=url,
            headers=self._auth_headers
        )

        if response.status_code == 429:
            self._handle_api_limit()

        if response.status_code != 200:  # Missing API limits handler and paging
            logging.warning("Unknown status code: %s", response.status_code)
            raise GitApiUnknownStatusCode

        try:
            return json_loads(response.content)
        except ValueError:
            logging.warning("Error while parsing json response.")
            raise GitApiResponseParsingError

    def get_user_info(self) -> Optional[Dict]:
        return self._handle_user_api_call(GitApiConstants.user_info_url.value)

    def get_all_user_orgs(self) -> Optional[List[Dict]]:
        return self._handle_user_api_call(GitApiConstants.user_orgs_url.value)

    def get_all_user_repos(self) -> Optional[List[Dict]]:
        return self._handle_user_api_call(GitApiConstants.user_repos_url.value)

    def get_all_repo_branches(self, username: str, repo_name: str) -> Optional[List[Dict]]:
        return self._handle_user_api_call(GitApiConstants.repo_branches_url_format.value.format(
            username=username,
            repo_name=repo_name,
        ))

    def get_all_commits_for_branch(self, username: str, repo_name: str, branch_sha: str) -> Optional[List[Dict]]:
        return self._handle_user_api_call(GitApiConstants.branch_commits_url_format.value.format(
            username=username,
            repo_name=repo_name,
            branch_sha=branch_sha,
        ))

    def check_rate_limit(self) -> Optional[Dict]:
        return self._handle_user_api_call(GitApiConstants.rate_limit_url.value)


