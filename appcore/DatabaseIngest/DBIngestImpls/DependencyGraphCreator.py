from zipfile import ZipInfo
from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface
from typing import List


class DependencyGraphCreator(DBIngestInterface):
    def create_db_objects(self, data: List[ZipInfo]):
        pass
