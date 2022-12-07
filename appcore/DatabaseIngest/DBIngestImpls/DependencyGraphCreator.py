from zipfile import ZipInfo
from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface
from typing import List
from appcore.DatabaseIngest.DBIngestImpls.CodeAnalysisImpls.PythonCodeAnalyser import PythonCodeAnalyser


class DependencyGraphCreator(DBIngestInterface):
    def __init__(self):
        self._import_analyser_list = [PythonCodeAnalyser()]

    def run(self, data: List[ZipInfo]):
        for file_info in data:
            analyser_input_data = {"filename": file_info.filename}
            for analyser in self._import_analyser_list:
                if analyser.can_analyse_file(analyser_input_data):
                    analyser.analyse_imports(analyser_input_data)
