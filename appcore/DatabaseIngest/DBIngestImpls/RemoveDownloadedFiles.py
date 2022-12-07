from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface
from typing import Dict
from os import remove as remove_file
from shutil import rmtree
from appcore.GitUtils.GitFileUtils import GitFileConstants

class RemoveDownloadedFiles(DBIngestInterface):
    def run(self, data: Dict) -> None:
        filename = data.get("filename")
        extracted_file = data.get("extracted_file")
        remove_file(GitFileConstants.REPO_DOWNLOAD_FILEPATH.value.format(filename=filename))
        rmtree(GitFileConstants.REPO_DOWNLOAD_EXTRACTION_FILEPATH.value + f'/{extracted_file}')
