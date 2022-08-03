from zipfile import ZipFile, ZipInfo
from enum import Enum
from typing import List, Optional, Dict, Tuple
from appcore.Exceptions.GitApiExceptions import GitApiLimit, GitApiResponseParsingError, GitApiUnknownStatusCode, GitApiJSONParsingError
from json import loads as json_loads
from requests import get as requests_get
from requests.structures import CaseInsensitiveDict
from urllib.parse import urljoin
from lxml import html
import logging


class GitFileConstants(Enum):
    github_filetree_url_format: str = "https://github.com/{username}/{repo_name}/find/{commit_sha}"
    filetree_xpath: str = '//virtual-filter-input[@aria-owns="tree-finder-results"]/@src'
    repo_download_url_format: str = "https://api.github.com/repos/{username}/{repo_name}/zipball/{commit_sha}"
    repo_download_filepath: str = "/usr/src/appcore/ClonedRepos/{filename}"
    repo_download_extraction_filepath: str = "/usr/src/appcore/ClonedRepos/Extracted"


class GitFileUtils:
    def __init__(self, access_token=None):
        self._access_token = access_token
        self._auth_headers_without_accept = {
            "Authorization": f"token {access_token}"
        }
        self._auth_headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {access_token}"
        }
        self._requested_with_headers = {
            "X-Requested-With": "XMLHttpRequest"
        }
    
    def _check_user_api_limit(self):
        pass

    def _handle_api_limit(self):
        logging.warning("User API limit reached.")
        raise GitApiLimit  # Missing database sync for storing user timeout

    def _handle_xpath_request(self, url: str, xpath: str) -> Optional[Dict]:
        self._check_user_api_limit()
        response = requests_get(
            url=url,
            headers=self._auth_headers_without_accept
        )

        if response.status_code == 429:
            self._handle_api_limit()

        if response.status_code != 200:  # Missing API limits handler and paging
            logging.warning("Unknown status code: %s", response.status_code)
            raise GitApiUnknownStatusCode

        document = html.fromstring(response.content)
        try:
            next_url = document.xpath(xpath)[0]
        except IndexError:
            logging.warning("Error while parsing html response.")
            raise GitApiResponseParsingError

        next_response = requests_get(
            url=urljoin(url, next_url),
            headers={**self._auth_headers_without_accept, **self._requested_with_headers}
        )
        try:
            return json_loads(next_response.content)
        except ValueError:
            logging.warning("Error while parsing json response.")
            raise GitApiJSONParsingError

    def _handle_raw_api_call(self, url: str) -> Optional[Tuple[bytes, CaseInsensitiveDict[str]]]:
        self._check_user_api_limit()
        response = requests_get(
            url=url,
            headers=self._auth_headers, allow_redirects=True
        )

        if response.status_code == 429:
            self._handle_api_limit()

        if response.status_code != 200:  # Missing API limits handler and paging
            logging.warning("Unknown status code: %s", response.status_code)
            raise GitApiUnknownStatusCode

        return response.content, response.headers

    def get_filetree_from_github(self, username: str, repo_name: str, commit_sha: str) -> List:
        return self._handle_xpath_request(GitFileConstants.github_filetree_url_format.value.format(
            username=username,
            repo_name=repo_name,
            commit_sha=commit_sha,
        ), GitFileConstants.filetree_xpath.value).get("paths")

    def get_files_from_api(self, username: str, repo_name: str, commit_sha: str):  # Maybe there is no point doing this
        pass

    def get_files_from_downloaded_zip(self, username: str, repo_name: str, commit_sha: str) -> List[ZipInfo]:
        response_content, response_headers = self._handle_raw_api_call(
            GitFileConstants.repo_download_url_format.value.format(
                username=username,
                repo_name=repo_name,
                commit_sha=commit_sha,
            ))

        filename = dict(response_headers).get("content-disposition").split("; ")[-1].replace("filename=", "")
        open(GitFileConstants.repo_download_filepath.value.format(filename=filename), "wb").write(response_content)

        filetree: List[ZipInfo] = []
        with ZipFile(GitFileConstants.repo_download_filepath.value.format(filename=filename), "r") as zipf:
            zipf.extractall(GitFileConstants.repo_download_extraction_filepath.value)
            filetree = zipf.filelist
            
        return filename, filetree
