import logging
from enum import Enum
from json import loads as json_loads
from typing import Optional, List, Dict
from urllib.parse import quote_plus

from lxml import html
from requests import get as requests_get

from backend.GitBackendUtils.GitApiExceptions import GitApiLimit, GitApiResponseParsingError, GitApiUnknownStatusCode


class GitApiConstants(Enum):
    user_info_url: str = "https://api.github.com/user"
    user_repos_url: str = "https://api.github.com/user/repos?per_page=100&sort=pushed"
    user_orgs_url: str = "https://api.github.com/user/orgs?per_page=100"
    user_starred_repos_url: str = "https://api.github.com/user/starred?per_page=100"
    repo_branches_url_format: str = "https://api.github.com/repos/{username}/{repo_name}/branches?per_page=100"
    branch_commits_url_format: str = (
        "https://api.github.com/repos/{username}/{repo_name}/commits?sha={" "branch_sha}&per_page=100"
    )
    repo_languages_url_format: str = "https://api.github.com/repos/{user_repo}/languages"
    rate_limit_url: str = "https://api.github.com/rate_limit"
    trending_repos_url: str = "https://github.com/trending"
    search_repos_url_format: str = "https://api.github.com/search/repositories?q={query}&per_page=100"
    max_page = 10


class GitApiUtils:
    def __init__(self, access_token=""):
        self._access_token = access_token
        self._auth_headers = {"Authorization": "token " + access_token, "Accept": "application/vnd.github.v3+json"}

    def _check_user_api_limit(self):
        pass

    def _handle_api_limit(self):
        logging.warning("User API limit reached.")
        raise GitApiLimit  # Missing database sync for storing user timeout

    def _handle_user_api_call(self, url: str) -> Optional[Dict]:
        self._check_user_api_limit()
        response = requests_get(url=url, headers=self._auth_headers)

        if response.status_code == 429:
            self._handle_api_limit()

        if response.status_code != 200:  # Missing API limits handler and paging
            logging.warning("Unknown status code: %s", response.status_code)
            raise GitApiUnknownStatusCode

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

    def _handle_multiple_page_api_call(self, url: str, start_page: int) -> Optional[List[Dict]]:
        repos = []
        page = start_page
        while True:
            data = self._handle_user_api_call(url + f"&page={page}")
            repo_data, more_pages = data.get("data", []), data.get("more_pages", False)
            repos.extend(repo_data)

            if not more_pages or page > GitApiConstants.max_page.value:
                break

            page += 1

        return repos

    def get_user_info(self) -> Optional[Dict]:
        return self._handle_user_api_call(GitApiConstants.user_info_url.value).get("data", {})

    def get_all_user_orgs(self) -> Optional[List[Dict]]:
        return self._handle_user_api_call(GitApiConstants.user_orgs_url.value).get("data", [])

    def get_all_user_repos(self, first_page_only=True, start_page=1) -> Optional[List[Dict]]:
        if first_page_only:
            return self._handle_user_api_call(GitApiConstants.user_repos_url.value).get("data", [])
        else:
            return self._handle_multiple_page_api_call(GitApiConstants.user_repos_url.value, start_page=start_page)

    def get_all_repo_branches(self, username: str, repo_name: str) -> Optional[List[Dict]]:
        return self._handle_user_api_call(
            GitApiConstants.repo_branches_url_format.value.format(
                username=username,
                repo_name=repo_name,
            )
        ).get("data", [])

    def get_all_commits_for_branch(self, username: str, repo_name: str, branch_sha: str) -> Optional[List[Dict]]:
        return self._handle_user_api_call(
            GitApiConstants.branch_commits_url_format.value.format(
                username=username,
                repo_name=repo_name,
                branch_sha=branch_sha,
            )
        ).get("data", [])

    def get_all_starred_repos(self, first_page_only=True, start_page=1) -> Optional[List[Dict]]:
        if first_page_only:
            return self._handle_user_api_call(GitApiConstants.user_starred_repos_url.value).get("data", [])
        else:
            return self._handle_multiple_page_api_call(
                GitApiConstants.user_starred_repos_url.value, start_page=start_page
            )

    def get_repo_languages(self, user_repo: str) -> Optional[Dict]:
        return self._handle_user_api_call(
            GitApiConstants.repo_languages_url_format.value.format(
                user_repo=user_repo,
            )
        ).get("data", {})

    def get_trending_repos(self) -> Optional[List[Dict]]:
        response = requests_get(GitApiConstants.trending_repos_url.value)
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
                GitApiConstants.search_repos_url_format.value.format(
                    query=quote_plus(query + " in:name,description,readme"),
                )
            )
            .get("data", {})
            .get("items", [])
        )

    def check_rate_limit(self) -> Optional[Dict]:
        return self._handle_user_api_call(GitApiConstants.rate_limit_url.value).get("data", {})
