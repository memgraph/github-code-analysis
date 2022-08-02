from zipfile import ZipInfo
from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface
from appcore.KafkaClient.CoreKafkaProducer import CoreKafkaProducer
from typing import List, Dict


class FileTreeCreator(DBIngestInterface):
    def __init__(self):
        super().__init__()
        self._kafka_producer = CoreKafkaProducer()

    def extract_files(self, file: ZipInfo) -> Dict:
        directories_before = []
        filename_splitted = file.filename.split("/")
        for index, file_name in enumerate(filename_splitted[:-1]):
            directories_before.append({"id": f"d{index}", "data": {"name": file_name, "path": "/".join(filename_splitted[:index + 1])}})
        
        link_before = []
        for index in range(1, len(directories_before)):
            link_before.append({"id": f"l{index}", "source": f"d{index - 1}", "target": f"d{index}", "link_data": {}})

        filename = file.filename.split("/")[-1]
        file_size = file.file_size

        after = {}
        link_after = {}

        if filename != "":
            after = {"id": "f0", "data": {"name": filename, "size": file_size, "path": file.filename}}
            link_after = {"id": "l0", "source": f"d{len(directories_before) - 1}", "target": "f0", "link_data": {}}
        
        return {"before": directories_before, 
                "link_before": link_before, 
                "after": after,
                "link_after": link_after}

    def run(self, data: List[ZipInfo]) -> None:
        for file in data:
            self._kafka_producer.produce_db_objects({"type": "filetree", "data": self.extract_files(file)})
