from typing import Optional, Tuple, Dict
from requests import get as requests_get
from json import loads as json_loads
from lxml import html
from urllib.parse import urljoin
from requests.structures import CaseInsensitiveDict


class GitUtils:
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

    def _handle_user_api_call(self, url: str) -> Optional[Dict]:
        response = requests_get(
            url=url,
            headers=self._auth_headers
        )
        if response.status_code != 200:  # Missing API limits handler and paging
            return None

        try:
            return json_loads(response.content)
        except ValueError:
            return None

    def _handle_xpath_request(self, url: str, xpath: str) -> Optional[Dict]:
        response = requests_get(
            url=url,
            headers=self._auth_headers_without_accept
        )
        document = html.fromstring(response.content)
        try:
            next_url = document.xpath(xpath)[0]
        except IndexError:
            return None

        next_response = requests_get(
            url=urljoin(url, next_url),
            headers={**self._auth_headers_without_accept, **self._requested_with_headers}
        )
        try:
            return json_loads(next_response.content)
        except ValueError:
            return None

    def _handle_raw_api_call(self, url: str) -> Optional[Tuple[bytes, CaseInsensitiveDict[str]]]:
        response = requests_get(
            url=url,
            headers=self._auth_headers, allow_redirects=True
        )
        if response.status_code != 200:  # Missing API limits handler and paging
            return None

        return response.content, response.headers

    def set_access_token(self, access_token):
        self._access_token = access_token
