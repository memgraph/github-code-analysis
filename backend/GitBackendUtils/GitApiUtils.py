import logging
from enum import Enum
from json import loads as json_loads
from typing import Optional, List, Dict
from urllib.parse import quote_plus

from lxml import html
from requests import get as requests_get

from backend.GitBackendUtils.GitApiExceptions import GitApiLimit, GitApiResponseParsingError, GitApiUnknownStatusCode


class GitApiConstants(Enum):
    MAX_PAGE = 10
    MAX_PER_PAGE = 100
    USER_INFO_URL: str = "https://api.github.com/user"
    USER_REPOS_URL: str = f"https://api.github.com/user/repos?per_page={MAX_PER_PAGE}&sort=pushed"
    USER_ORGS_URL: str = f"https://api.github.com/user/orgs?per_page={MAX_PER_PAGE}"
    USER_STARRED_REPOS_URL: str = f"https://api.github.com/user/starred?per_page={MAX_PER_PAGE}"
    REPO_DETAILS_URL_FORMAT: str = "https://api.github.com/repos/{full_name}?per_page="+str(MAX_PER_PAGE)
    REPO_BRANCHES_URL_FORMAT: str = "https://api.github.com/repos/{user_repo}/branches?per_page="+str(MAX_PER_PAGE)
    BRANCH_COMMITS_URL_FORMAT: str = (
        "https://api.github.com/repos/{user_repo}/commits?sha={branch_sha}&per_page="+str(MAX_PER_PAGE)
    )
    REPO_LANGUAGES_URL_FORMAT: str = "https://api.github.com/repos/{user_repo}/languages"
    RATE_LIMIT_URL: str = "https://api.github.com/rate_limit"
    TRENDING_REPOS_URL: str = "https://github.com/trending"
    SEARCH_REPOS_URL_FORMAT: str = "https://api.github.com/search/repositories?q={query}&per_page="+str(MAX_PER_PAGE)


class GitApiUtils:
    def __init__(self, access_token=""):
        self._access_token = access_token
        self._auth_headers = {"Authorization": "token " + access_token, "Accept": "application/vnd.github.v3+json"}

    def _check_user_api_limit(self):
        pass

    def _handle_api_limit(self):
        logging.warning("User API limit reached.")
        raise GitApiLimit  # Missing database sync for storing user timeout

    def handle_response_status_code(self, status_code: int):
        if status_code == 429:
            self._handle_api_limit()

        if status_code != 200:  # Missing API limits handler and paging
            logging.warning("Unknown status code: %s", status_code)
            raise GitApiUnknownStatusCode

    def _handle_user_api_call(self, url: str) -> Optional[Dict]:
        self._check_user_api_limit()
        response = requests_get(url=url, headers=self._auth_headers)

        self.handle_response_status_code(response.status_code)

        try:
            return {
                "data": json_loads(response.content),
                "more_pages": dict(response.headers).get("Link") is not None,
            }
        except ValueError:
            logging.warning("Error while parsing json response.")
            raise GitApiResponseParsingError

    def _handle_unauthenticated_api_call(self, url: str) -> Optional[Dict]:
        response = requests_get(url=url, headers={"Accept": "application/vnd.github.v3+json"})

        self.handle_response_status_code(response.status_code)

        try:
            return json_loads(response.content)
        except ValueError:
            logging.warning("Error while parsing json response.")
            raise GitApiResponseParsingError

    def _handle_multiple_page_api_call(self, url: str, start_page: int) -> Optional[List[Dict]]:
        repos = []
        page = start_page
        while True:
            data = self._handle_user_api_call(url + f"&page={page}")
            repo_data, more_pages = data.get("data", []), data.get("more_pages", False)
            repos.extend(repo_data)

            if not more_pages or page > GitApiConstants.MAX_PAGE.value:
                break

            page += 1

        return repos

    def get_user_info(self) -> Optional[Dict]:
        return self._handle_user_api_call(GitApiConstants.USER_INFO_URL.value).get("data", {})

    def get_all_user_orgs(self) -> Optional[List[Dict]]:
        return self._handle_user_api_call(GitApiConstants.USER_ORGS_URL.value).get("data", [])

    def get_all_user_repos(self, first_page_only=True, start_page=1) -> Optional[List[Dict]]:
        if first_page_only:
            return self._handle_user_api_call(GitApiConstants.USER_REPOS_URL.value).get("data", [])
        else:
            return self._handle_multiple_page_api_call(GitApiConstants.USER_REPOS_URL.value, start_page=start_page)

    def get_all_repo_branches(self, user_repo: str, first_page_only=True, start_page=1) -> Optional[List[Dict]]:
        if first_page_only:
            return self._handle_user_api_call(
                GitApiConstants.REPO_BRANCHES_URL_FORMAT.value.format(
                    user_repo=user_repo,
                )
            ).get("data", [])
        else:
            return self._handle_multiple_page_api_call(
                GitApiConstants.REPO_BRANCHES_URL_FORMAT.value.format(
                    user_repo=user_repo,
                ), start_page=start_page
            )

    def get_all_commits_for_branch(self, user_repo: str, branch_sha: str) -> Optional[List[Dict]]:
        return self._handle_user_api_call(
            GitApiConstants.BRANCH_COMMITS_URL_FORMAT.value.format(
                user_repo=user_repo,
                branch_sha=branch_sha,
            )
        ).get("data", [])

    def get_all_starred_repos(self, first_page_only=True, start_page=1) -> Optional[List[Dict]]:
        if first_page_only:
            return self._handle_user_api_call(GitApiConstants.USER_STARRED_REPOS_URL.value).get("data", [])
        else:
            return self._handle_multiple_page_api_call(
                GitApiConstants.USER_STARRED_REPOS_URL.value, start_page=start_page
            )

    def get_repo_languages(self, user_repo: str) -> Optional[Dict]:
        return self._handle_user_api_call(
            GitApiConstants.REPO_LANGUAGES_URL_FORMAT.value.format(
                user_repo=user_repo,
            )
        ).get("data", {})

    def get_trending_repos(self) -> Optional[List[Dict]]:
        response = requests_get(GitApiConstants.TRENDING_REPOS_URL.value)
        document = html.fromstring(response.content)
        return list(
            map(
                lambda repo: {
                    "full_name": repo.xpath("./h1/a/@href")[0][1:],
                    "description": "".join(repo.xpath("./p/text()")).strip(),
                    "stars": int(
                        repo.xpath("./div/a[contains(@href, 'stargazers')]/text()")[-1].strip().replace(",", "")
                    ),
                    "stars_today": int(
                        repo.xpath("./div/span[@class='d-inline-block float-sm-right']/text()")[-1]
                        .strip()
                        .split()[0]
                        .replace(",", "")
                    ),
                    "language": "".join(repo.xpath(".//span[@itemprop='programmingLanguage']/text()")),
                    "github_url": "https://github.com" + repo.xpath("./h1/a/@href")[0],
                },
                document.xpath("//div/article[@class='Box-row']")[:-1],
            )
        )

    def search_for_repos(self, query: str) -> Optional[List[Dict]]:
        return (
            self._handle_user_api_call(
                GitApiConstants.SEARCH_REPOS_URL_FORMAT.value.format(
                    query=quote_plus(query + " in:name,description,readme"),
                )
            )
            .get("data", {})
            .get("items", [])
        )

    def repo_exists(self, full_name: str) -> bool:
        try:
            repo = self._handle_user_api_call(GitApiConstants.REPO_DETAILS_URL_FORMAT.value.format(full_name=full_name))
            return repo.get("data", {}).get("full_name", "") == full_name

        except GitApiUnknownStatusCode or GitApiResponseParsingError or GitApiLimit:
            return False

    def get_single_repo_info(self, full_name: str) -> Optional[Dict]:
        return self._handle_user_api_call(GitApiConstants.REPO_DETAILS_URL_FORMAT.value.format(full_name=full_name)).get("data", {})

    def check_rate_limit(self) -> Optional[Dict]:
        return self._handle_user_api_call(GitApiConstants.RATE_LIMIT_URL.value).get("data", {})
