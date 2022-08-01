from kafka import KafkaProducer
from json import dumps
from appcore.KafkaClient.CoreKafkaConstants import CoreKafkaConstants
from typing import Dict


class CoreKafkaProducer:
    def __init__(self):
        self._producer = KafkaProducer(bootstrap_servers=f"{CoreKafkaConstants.KAFKA_IP.value}:" \
                                                         f"{CoreKafkaConstants.KAFKA_PORT.value}",
                                       value_serializer=lambda x:
                                       dumps(x).encode('utf-8'))

    def produce_db_objects(self, data: Dict):
        self._producer.send(CoreKafkaConstants.KAFKA_PRODUCER_TOPIC_NAME.value, data)

    def __del__(self):
        self._producer.close()
