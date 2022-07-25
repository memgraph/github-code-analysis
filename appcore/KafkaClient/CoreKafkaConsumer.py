from enum import Enum
from appcore.KafkaClient.QueryParsing import QueryParsing
from kafka import KafkaConsumer
from time import sleep
import logging
from multiprocessing import Process


class CoreKafkaConstants(Enum):
    KAFKA_CONSUMER_IP: str = "broker"
    KAFKA_CONSUMER_PORT: str = "9092"
    KAFKA_TOPIC_NAME: str = "to_core_data"
    KAFKA_DOWNLOAD_AND_GET_ALL_FORMAT: str = '{{"query_type": "download_and_get_all", "username": "{username}", "repo_name": "{repo_name}", "commit_sha": "{commit_sha}", "access_token": "{access_token}"}}'


class CoreKafkaConsumer:
    @staticmethod
    def run():
        consumer = KafkaConsumer(
            bootstrap_servers=f"{CoreKafkaConstants.KAFKA_CONSUMER_IP.value}:" \
                              f"{CoreKafkaConstants.KAFKA_CONSUMER_PORT.value}",
            auto_offset_reset="latest"
        )
        consumer.subscribe([CoreKafkaConstants.KAFKA_TOPIC_NAME.value])
        for message in consumer:
            Process(target=QueryParsing.recognize, args=(message.value,)).start()
        consumer.close()


if __name__ == "__main__":
    sleep(4)
    logging.basicConfig(filename=f"appcore/Log/logfile.txt",
                        level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    CoreKafkaConsumer.run()
