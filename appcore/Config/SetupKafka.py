from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable
from appcore.KafkaClient.CoreKafkaConstants import CoreKafkaConstants
import logging
from time import sleep


class SetupKafka:
    @staticmethod
    def run():
        found_broker = False
        while not found_broker:
            try:
                admin_client = KafkaAdminClient(
                    bootstrap_servers=f"{CoreKafkaConstants.KAFKA_IP.value}:{CoreKafkaConstants.KAFKA_PORT.value}", 
                )
                found_broker = True
            except NoBrokersAvailable:
                logging.error("NoBrokersAvailable")
                sleep(1)

        topic_list = []
        topic_list.append(NewTopic(name=CoreKafkaConstants.KAFKA_CONSUMER_TOPIC_NAME.value, num_partitions=1, replication_factor=1))
        topic_list.append(NewTopic(name=CoreKafkaConstants.KAFKA_PRODUCER_TOPIC_NAME.value, num_partitions=1, replication_factor=1))
        for topic in topic_list:
            try:
                admin_client.create_topics(new_topics=[topic], validate_only=False)
            except TopicAlreadyExistsError:
                pass

        admin_client.close()
