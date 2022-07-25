from zipfile import ZipFile, ZipInfo
from enum import Enum
from appcore.GitUtils.GitUtils import GitUtils


class GitFileConstants(Enum):
    github_filetree_url_format: str = "https://github.com/{username}/{repo_name}/find/{commit_sha}"
    filetree_xpath: str = '//virtual-filter-input[@aria-owns="tree-finder-results"]/@src'
    repo_download_url_format: str = "https://api.github.com/repos/{username}/{repo_name}/zipball/{commit_sha}"
    repo_download_filepath: str = "/usr/src/appcore/ClonedRepos/{filename}"
    repo_download_extraction_filepath: str = "/usr/src/appcore/ClonedRepos/Extracted"


class GitFileUtils(GitUtils):
    def __init__(self, access_token=None):
        super().__init__(access_token)

    def get_filetree_from_github(self, username: str, repo_name: str, commit_sha: str) -> list:
        return self._handle_xpath_request(GitFileConstants.github_filetree_url_format.value.format(
            username=username,
            repo_name=repo_name,
            commit_sha=commit_sha,
        ), GitFileConstants.filetree_xpath.value).get("paths")  # This is very bad and I'll implement something better

    def get_files_from_api(self, username: str, repo_name: str, commit_sha: str):  # Maybe there is no point doing this
        pass

    def get_files_from_downloaded_zip(self, username: str, repo_name: str, commit_sha: str) -> list[ZipInfo]:
        response_content, response_headers = self._handle_raw_api_call(
            GitFileConstants.repo_download_url_format.value.format(
                username=username,
                repo_name=repo_name,
                commit_sha=commit_sha,
            ))
        filename = dict(response_headers).get("content-disposition").split("; ")[-1].replace("filename=", "")
        open(GitFileConstants.repo_download_filepath.value.format(filename=filename), "wb").write(response_content)
        filetree: [ZipInfo] = []
        with ZipFile(GitFileConstants.repo_download_filepath.value.format(filename=filename), "r") as zipf:
            zipf.extractall(GitFileConstants.repo_download_extraction_filepath.value)
            filetree = zipf.filelist
        return filetree
