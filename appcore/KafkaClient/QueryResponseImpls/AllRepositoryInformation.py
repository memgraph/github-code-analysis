from appcore.KafkaClient.QueryResponseInterface import QueryResponseInterface
from appcore.DatabaseIngest.DBIngestRunner import DBIngestRunner
from appcore.GitUtils.GitFileUtils import GitFileUtils
import logging
from typing import Dict


class AllRepositoryInformation(QueryResponseInterface):
    @staticmethod
    def query_response(query: Dict) -> None:
        username = query.get("username")
        repo_name = query.get("repo_name")
        commit_sha = query.get("commit_sha")
        access_token = query.get("access_token")

        if not username or not repo_name or not commit_sha or not access_token:
            logging.warning("Missing username, repo_name, commit_sha or access_token.")
            return

        git_file_utils = GitFileUtils(access_token=access_token)
        filename, filetree = git_file_utils.get_files_from_downloaded_zip(
            username=username,
            repo_name=repo_name,
            commit_sha=commit_sha,
        )
        try:
            DBIngestRunner.run_beginning_methods(filename=filename, filetree=filetree[0].filename, commit_sha=commit_sha)
            DBIngestRunner.run_filetree(filetree=filetree)
            DBIngestRunner.run_branches_and_commits()
        except Exception as e:
            print(e)
        finally:
            DBIngestRunner.run_finishing_methods(filename=filename, filetree=filetree[0].filename, commit_sha=commit_sha)
