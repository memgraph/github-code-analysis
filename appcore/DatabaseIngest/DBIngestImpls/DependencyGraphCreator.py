from zipfile import ZipInfo
from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface


class DependencyGraphCreator(DBIngestInterface):
    def create_db_objects(self, data: list[ZipInfo]):
        pass
