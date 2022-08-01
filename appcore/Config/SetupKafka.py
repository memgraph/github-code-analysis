from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from appcore.KafkaClient.CoreKafkaConstants import CoreKafkaConstants


class SetupKafka:
    @staticmethod
    def run():
        admin_client = KafkaAdminClient( # handle kafka.errors.NoBrokersAvailable; best with while loop
            bootstrap_servers=f"{CoreKafkaConstants.KAFKA_IP.value}:{CoreKafkaConstants.KAFKA_PORT.value}", 
        )

        topic_list = []
        topic_list.append(NewTopic(name=CoreKafkaConstants.KAFKA_CONSUMER_TOPIC_NAME.value, num_partitions=1, replication_factor=1))
        topic_list.append(NewTopic(name=CoreKafkaConstants.KAFKA_PRODUCER_TOPIC_NAME.value, num_partitions=1, replication_factor=1))
        for topic in topic_list:
            try:
                admin_client.create_topics(new_topics=[topic], validate_only=False)
            except TopicAlreadyExistsError:
                pass
