from enum import Enum
from re import match, findall
from typing import Dict

from appcore.DatabaseIngest.DBIngestImpls.CodeAnalysisImpls.ImportsAnalyserInterface import ImportsAnalyserInterface
from appcore.DatabaseIngest.DBIngestImpls.CodeAnalysisImpls.LanguageTypeCheckerInterface import \
    LanguageTypeCheckerInterface
from appcore.GitUtils.GitFileUtils import GitFileConstants
from appcore.KafkaClient.CoreKafkaProducer import CoreKafkaProducer


class PythonRegexConstants(Enum):
    REMOVE_AS_REGEX: str = rb"((\w+)[ ]+as[ ]+(\w+))"
    FROM_IMPORT_REGEX: str = rb"^from\s+([\w.]+)\s+import\s*([\w, ]*)"
    NUMBER_OF_DOTS_REGEX: str = rb"(^[.]*)"
    IMPORT_REGEX: str = rb"^import\s+([\w ,]+)"
    STRING_SINGLE_QUOTATION_REGEX: str = rb"(\'.*\')"
    STRING_DOUBLE_QUOTATION_REGEX: str = rb"(\".*\")"


def _extract_filename_from_data(data: Dict) -> str:
    return data.get("filename")


class PythonCodeAnalyser(ImportsAnalyserInterface, LanguageTypeCheckerInterface):
    def __init__(self):
        self._kafka_producer = CoreKafkaProducer()

    def can_analyse_file(self, data: Dict) -> bool:
        filename = _extract_filename_from_data(data)
        if filename.endswith(".py"):
            return True
        return False

    def import_is_called(self, code: str, import_name: str) -> int:
        return code.count(import_name)

    def analyse_imports(self, data: Dict) -> None:
        filename = f"{GitFileConstants.REPO_DOWNLOAD_EXTRACTION_FILEPATH.value}/{_extract_filename_from_data(data)}"
        imports = {}
        translation_layer = {}
        code = []
        with open(filename, 'rb') as opened_file:
            more_lines = False
            current_import = None
            for line in opened_file.readlines():
                line = line.replace(b'\n', b'').split(b"#")[0].strip()
                code.append(line)
                remove_as = findall(PythonRegexConstants.REMOVE_AS_REGEX.value, line)
                for original, remove, replaced in remove_as:
                    line = line.replace(remove, b"")

                if more_lines:
                    for original, remove, replaced in remove_as:
                        translation_layer[original] = replaced

                    matched_imports = findall(rb"(\w+)", line)
                    for matched_import in matched_imports:
                        imports[current_import][matched_import] = 0

                    if line.endswith(b"\\"):
                        more_lines = True
                        continue

                    if line.endswith(b","):
                        more_lines = True
                        continue

                    if line.endswith(b")"):
                        more_lines = False
                        continue

                    more_lines = False
                    continue

                from_import_match = match(PythonRegexConstants.FROM_IMPORT_REGEX.value, line)
                if from_import_match is not None:
                    for original, remove, replaced in remove_as:
                        translation_layer[original] = replaced
                    files = from_import_match.group(1)
                    if files.startswith(b"."):
                        number_of_dots = match(PythonRegexConstants.NUMBER_OF_DOTS_REGEX.value, files).group(1).count(b".")
                        files = b".".join(_extract_filename_from_data(data).encode("utf-8").split(b"/")[:number_of_dots*(-1)]) + b"." + files[number_of_dots:]
                    if b"\\" in line or b"(" in line:
                        more_lines = True
                        current_import = files
                    imports[files] = {}
                    imported_stuff = from_import_match.group(2)
                    if imported_stuff:
                        for imported in imported_stuff.replace(b" ", b"").split(b","):
                            imports[files][imported] = 0
                    continue

                elif match(PythonRegexConstants.IMPORT_REGEX.value, line):
                    for original, remove, replaced in remove_as:
                        translation_layer[original] = replaced
                    files = match(PythonRegexConstants.IMPORT_REGEX.value, line).group(1)
                    imports[files] = 0
                    if b"\\" in line or b"(" in line:
                        more_lines = True
                        current_import = None

                    continue

            joined_code = b' '.join(code)

            for big_string in findall(PythonRegexConstants.STRING_DOUBLE_QUOTATION_REGEX.value, joined_code):
                joined_code = joined_code.replace(big_string, b"")

            for big_string in findall(PythonRegexConstants.STRING_SINGLE_QUOTATION_REGEX.value, joined_code):
                joined_code = joined_code.replace(big_string, b"")

            memgraph_imports = {}

            for key, item in imports.items():
                decoded_key = key.decode("utf-8").replace(".", "/") + ".py"
                if type(item) is dict:
                    for key2 in item.keys():
                        import_to_match = translation_layer.get(key2, key2)
                        if decoded_key not in memgraph_imports:
                            memgraph_imports[decoded_key] = {}
                        memgraph_imports[decoded_key][key2.decode("utf-8")] = self.import_is_called(joined_code, import_to_match)

                else:
                    import_to_match = translation_layer.get(key, key)
                    memgraph_imports[decoded_key] = self.import_is_called(joined_code, import_to_match)

        self._kafka_producer.produce_db_objects({"type": "imports_dependency",
                                                 "data": {
                                                     "imports": memgraph_imports,
                                                     "filename": _extract_filename_from_data(data),
                                                     "root_path": _extract_filename_from_data(data).split("/")[0],
                                                 }})
