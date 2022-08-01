from kafka import KafkaConsumer
from appcore.KafkaClient.CoreKafkaConstants import CoreKafkaConstants



consumer = KafkaConsumer(
            bootstrap_servers=f"{CoreKafkaConstants.KAFKA_IP.value}:" \
                              f"{CoreKafkaConstants.KAFKA_PORT.value}",
            auto_offset_reset="latest"
        )
consumer.subscribe([CoreKafkaConstants.KAFKA_PRODUCER_TOPIC_NAME.value])
for message in consumer:  # Error handling is missing
    print(message)