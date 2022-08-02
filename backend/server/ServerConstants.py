from enum import Enum


class ServerConstants(Enum):
    KAFKA_DOWNLOAD_AND_GET_ALL_FORMAT: str = '{{"query_type": "all_repository_information", "username": "{username}", "repo_name": "{repo_name}", "commit_sha": "{commit_sha}", "access_token": "{access_token}"}}'
    KAFKA_IP = "broker"
    KAFKA_PORT = "9092"
    KAFKA_TO_CORE_TOPIC = "to_core_data"
    LOGGING_FILE_PATH = "/usr/src/backend/server/log.txt"
