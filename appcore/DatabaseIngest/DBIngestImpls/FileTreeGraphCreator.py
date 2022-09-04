from zipfile import ZipInfo
from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface
from appcore.GitUtils.GitFileUtils import GitFileConstants
from appcore.KafkaClient.CoreKafkaProducer import CoreKafkaProducer
from typing import List, Dict
from hashlib import sha1


class FileTreeCreator(DBIngestInterface):
    def __init__(self):
        super().__init__()
        self._kafka_producer = CoreKafkaProducer()
        self._already_created_dirs = set()

    def extract_files(self, file: ZipInfo) -> Dict:
        directories_before = []
        filename_splitted = file.filename.split("/")
        link_before = []
        filename = file.filename.split("/")[-1]
        file_size = file.file_size
        after = {}
        link_after = {}

        if filename != "":
            with open(GitFileConstants.REPO_DOWNLOAD_EXTRACTION_FILEPATH.value + "/" + file.filename, 'rb') as opened_file:
                data = opened_file.read()
                hash_object = sha1(data)
                dir_to_connect_with = "/".join(filename_splitted[:-1])
                after = {"id": "f", "data": {"name": filename, "path": file.filename, "size": file_size, "file_hash": hash_object.hexdigest()}}
                link_after = {"id": "l", "source": dir_to_connect_with, "target": "f", "link_data": {}}
        else:
            for partial_filename_index in range(1, len(filename_splitted)):
                partial_filename = "/".join(filename_splitted[:partial_filename_index])
                if partial_filename not in self._already_created_dirs:
                    self._already_created_dirs.add(partial_filename)
                    directories_before.append(
                        {"id": f"d{partial_filename_index}",
                         "data": {"name": filename_splitted[partial_filename_index-1], "path": partial_filename}})
                    if partial_filename_index > 1:
                        dir_to_connect_with = "/".join(filename_splitted[:partial_filename_index-1])
                        link_before.append({"id": f"l{partial_filename_index}",
                                            "source": dir_to_connect_with, "target": partial_filename, "link_data": {}})
        
        return {"before": directories_before, 
                "link_before": link_before, 
                "after": after,
                "link_after": link_after}

    def run(self, data: List[ZipInfo]) -> None:
        if len(data) == 0:
            return

        self._already_created_dirs.add(data[0].filename.split("/")[0])

        for file in data:
            self._kafka_producer.produce_db_objects({"type": "filetree", "data": self.extract_files(file)})
