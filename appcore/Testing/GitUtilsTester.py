from typing import Optional, Tuple
from zipfile import ZipInfo

from appcore.GitUtils.GitFileUtils import GitFileUtils


class GitUtilsTester:
    def __init__(self, access_token: Optional[str] = None):
        self._git_file_client = GitFileUtils(access_token=access_token)

    def get_branch_by_name(self, branches: list[dict], name: str) -> Optional[dict]:
        if len(branches) == 0:
            return
        selected = branches[0]
        for branch in branches:
            if branch.get("name", "") == name:
                return branch

        return selected

    def get_sample_filetree(self, username: str, repo: str, commit_hash: str) -> Optional[list[ZipInfo]]:
        return self._git_file_client.get_files_from_downloaded_zip(
            username=username,
            repo_name=repo,
            commit_sha=commit_hash,
        )

    def dry_run(self) -> None:
        username, repo, branch = "Adri-Noir", "iOSMovieApp", "03640357b92c3342be5902e1b153b992f9618f1d"

        files = self._git_file_client.get_files_from_downloaded_zip(
            username=username,
            repo_name=repo,
            commit_sha=branch,
        )
        tree = self._git_file_client.get_filetree_from_github(
            username=username,
            repo_name=repo,
            commit_sha=branch,
        )
        print(username, repo, branch, sep="\n")
        print(files)
        print(tree)
