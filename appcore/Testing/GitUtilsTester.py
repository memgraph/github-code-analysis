from typing import Optional, Tuple
from zipfile import ZipInfo

from appcore.GitUtils.GitApiUtils import GitApiUtils
from appcore.GitUtils.GitFileUtils import GitFileUtils


class GitUtilsTester:
    def __init__(self, access_token: Optional[str] = None):
        self._git_file_client = GitFileUtils(access_token=access_token)
        self._git_api_client = GitApiUtils(access_token=access_token)

    def get_branch_by_name(self, branches: list[dict], name: str) -> Optional[dict]:
        if len(branches) == 0:
            return
        selected = branches[0]
        for branch in branches:
            if branch.get("name", "") == name:
                return branch

        return selected

    def get_sample_filetree(self, username: Optional[str] = None, repo: Optional[str] = None) -> Optional[list[ZipInfo]]:
        username, repo, branches = self.get_relevant_data(username=username, repo=repo)

        masterbranch = self.get_branch_by_name(branches, "master")

        return self._git_file_client.get_files_from_downloaded_zip(
            username=username,
            repo_name=repo,
            commit_sha=masterbranch.get("commit", {}).get("sha", ""),
        )

    def get_relevant_data(self, username: Optional[str] = None, repo: Optional[str] = None) -> Tuple[Optional[str], Optional[str], Optional[list[dict]]]:
        if username is None:
            user = self._git_api_client.get_user_info()
            if user is None:
                return None, None, None
            username = user.get("login")

            orgs = self._git_api_client.get_all_user_orgs()

        if repo is None:
            repos = self._git_api_client.get_all_user_repos()

            if len(repos) > 0:
                repo = repos[0].get("name")
                if repo is None:
                    return None, None, None
            else:
                return None, None, None
        branches = self._git_api_client.get_all_repo_branches(username=username, repo_name=repo)
        return username, repo, branches

    def dry_run(self) -> None:
        username, repo, branches = self.get_relevant_data()

        masterbranch = self.get_branch_by_name(branches, "master")
        files = self._git_file_client.get_files_from_downloaded_zip(
            username=username,
            repo_name=repo,
            commit_sha=masterbranch.get("commit", {}).get("sha", ""),
        )
        tree = self._git_file_client.get_filetree_from_github(
            username=username,
            repo_name=repo,
            commit_sha=masterbranch.get("commit", {}).get("sha", ""),
        )
        print(username, repo, masterbranch, sep="\n")
        print(files)
        print(tree)
