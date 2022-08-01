from enum import Enum


class CoreKafkaConstants(Enum):
    KAFKA_IP: str = "broker"
    KAFKA_PORT: str = "9092"
    KAFKA_CONSUMER_TOPIC_NAME: str = "to_core_data"
    KAFKA_PRODUCER_TOPIC_NAME: str = "to_memgraph_data"
    KAFKA_DOWNLOAD_AND_GET_ALL_FORMAT: str = '{{"query_type": "all_repository_information", "username": "{username}", "repo_name": "{repo_name}", "commit_sha": "{commit_sha}", "access_token": "{access_token}"}}'
