from kafka import KafkaProducer
from appcore.KafkaClient.CoreKafkaConsumer import CoreKafkaConstants
from os import getenv


class KafkaMockProducer:
    @staticmethod
    def mock_download_all() -> None:
        producer = KafkaProducer(bootstrap_servers='broker:9092')
        producer.send('to_core_data', CoreKafkaConstants.KAFKA_DOWNLOAD_AND_GET_ALL_FORMAT.value.format(
            username="kjkardum",
            repo_name="ios-projekt",
            commit_sha="8e703dfe436185aa73fe3b2443c16c449ef0913e",
            access_token=getenv("ACCESS_TOKEN")
        ).encode("utf-8"))
        producer.close()
        print("Mock download_and_get_all sent")
        return


if __name__ == "__main__":
    KafkaMockProducer.mock_download_all()
