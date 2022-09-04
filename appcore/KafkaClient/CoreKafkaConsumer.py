from appcore.KafkaClient.CoreKafkaConstants import CoreKafkaConstants
from appcore.KafkaClient.QueryParsing import QueryParsing
from kafka import KafkaConsumer
from multiprocessing import Process
from multiprocessing import Pool


class CoreKafkaConsumer:
    @staticmethod
    def run():
        pool = Pool(processes=100)
        consumer = KafkaConsumer(
            bootstrap_servers=f"{CoreKafkaConstants.KAFKA_IP.value}:" \
                              f"{CoreKafkaConstants.KAFKA_PORT.value}",
            auto_offset_reset="latest"
        )
        consumer.subscribe([CoreKafkaConstants.KAFKA_CONSUMER_TOPIC_NAME.value])
        for message in consumer:
            pool.apply_async(QueryParsing.recognize, args=(message.value,))

        pool.close()
        consumer.close()



if __name__ == "__main__":
    CoreKafkaConsumer.run()