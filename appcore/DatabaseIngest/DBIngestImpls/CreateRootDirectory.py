from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface
from typing import Dict
from appcore.KafkaClient.CoreKafkaProducer import CoreKafkaProducer


class CreateRootDirectory(DBIngestInterface):
    def __init__(self):
        super().__init__()
        self._kafka_producer = CoreKafkaProducer()

    def run(self, data: Dict) -> None:
        extracted_file = data.get("extracted_file").replace("/", "")

        self._kafka_producer.produce_db_objects({"type": "filetree", "data": {
            "before": [{"id": "root_dir", "data": {"name": extracted_file, "path": extracted_file, "size": 0}}],
            "link_before": [],
            "after": {},
            "link_after": {}}})