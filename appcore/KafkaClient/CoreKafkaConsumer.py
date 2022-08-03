from appcore.KafkaClient.CoreKafkaConstants import CoreKafkaConstants
from appcore.KafkaClient.QueryParsing import QueryParsing
from kafka import KafkaConsumer
from multiprocessing import Process


class CoreKafkaConsumer:
    @staticmethod
    def run():
        consumer = KafkaConsumer(
            bootstrap_servers=f"{CoreKafkaConstants.KAFKA_IP.value}:" \
                              f"{CoreKafkaConstants.KAFKA_PORT.value}",
            auto_offset_reset="latest"
        )
        consumer.subscribe([CoreKafkaConstants.KAFKA_CONSUMER_TOPIC_NAME.value])
        for message in consumer:
            QueryParsing.recognize(message.value)
            # Process(target=QueryParsing.recognize, args=(message.value,)).start()
        consumer.close()


if __name__ == "__main__":
    CoreKafkaConsumer.run()