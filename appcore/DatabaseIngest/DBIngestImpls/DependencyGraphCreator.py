from zipfile import ZipInfo
from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface
from typing import List


class DependencyGraphCreator(DBIngestInterface):
    def run(self, data: List[ZipInfo]):
        pass
