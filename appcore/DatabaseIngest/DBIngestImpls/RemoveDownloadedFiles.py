from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface
from typing import Tuple
from os import remove as remove_file
from shutil import rmtree
from appcore.GitUtils.GitFileUtils import GitFileConstants

class RemoveDownloadedFiles(DBIngestInterface):
    def run(self, data: Tuple[str, str]) -> None:
        filename, extracted_file = data
        remove_file(GitFileConstants.repo_download_filepath.value.format(filename=filename))
        rmtree(GitFileConstants.repo_download_extraction_filepath.value + f'/{extracted_file}')
