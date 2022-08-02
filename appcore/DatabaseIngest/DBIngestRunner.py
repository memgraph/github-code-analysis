from zipfile import ZipInfo
from appcore.DatabaseIngest.DBIngestImplsList import DBIngestImplsList
from typing import List


class DBIngestRunner:
    @staticmethod
    def run_filetree(filetree: List[ZipInfo]):
        for ingest in DBIngestImplsList.filetree_impls_list.value:
            runner = ingest()
            runner.run(data=filetree)

    @staticmethod
    def run_branches_and_commits():
        for ingest in DBIngestImplsList.commits_impls_list.value:
            runner = ingest()
            runner.run(branches=[])

    @staticmethod
    def run_finishing_methods(filename: str, filetree: str):
        for ingest in DBIngestImplsList.finishing_impls_list.value:
            runner = ingest()
            runner.run((filename, filetree))