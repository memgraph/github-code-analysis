from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface
from typing import Dict
from appcore.KafkaClient.CoreKafkaProducer import CoreKafkaProducer


class ConnectCommitAndFiles(DBIngestInterface):
    def __init__(self):
        super().__init__()
        self._kafka_producer = CoreKafkaProducer()

    def run(self, data: Dict) -> None:
        extracted_file = data.get("extracted_file")
        commit_sha = data.get("commit_sha")

        self._kafka_producer.produce_db_objects({"type": "connect_commit_file", "data": {"commit_sha": commit_sha, "extracted_file": extracted_file}})
