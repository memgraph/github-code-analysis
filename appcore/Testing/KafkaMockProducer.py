from kafka import KafkaProducer
from appcore.KafkaClient.CoreKafkaConsumer import CoreKafkaConstants
from os import getenv


class KafkaMockProducer:
    @staticmethod
    def mock_download_all() -> None:
        producer = KafkaProducer(bootstrap_servers='broker:9092')
        producer.send('to_core_data', CoreKafkaConstants.KAFKA_DOWNLOAD_AND_GET_ALL_FORMAT.value.format(
            username="Adri-Noir",
            repo_name="iOSMovieApp",
            commit_sha="03640357b92c3342be5902e1b153b992f9618f1d",
            access_token=getenv("ACCESS_TOKEN")
        ).encode("utf-8"))
        producer.close()
        print("Mock download_and_get_all sent")
        return


if __name__ == "__main__":
    KafkaMockProducer.mock_download_all()
