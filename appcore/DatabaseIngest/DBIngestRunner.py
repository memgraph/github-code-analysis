from zipfile import ZipInfo
from appcore.DatabaseIngest.DBIngestImplsList import DBIngestImplsList


class DBIngestRunner:
    @staticmethod
    def run_filetree(filetree: list[ZipInfo]):
        for ingest in DBIngestImplsList.filetree_impls_list.value:
            runner = ingest()
            runner.create_db_objects(data=filetree)

    @staticmethod
    def run_branches_and_commits():
        for ingest in DBIngestImplsList.commits_impls_list.value:
            runner = ingest()
            runner.create_db_objects(branches=[])
