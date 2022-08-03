from appcore.Config.SetupKafka import SetupKafka
from appcore.Config.SetupMemgraph import SetupMemgraph
from appcore.KafkaClient.CoreKafkaConsumer import CoreKafkaConsumer
from time import sleep
import logging


def setup():
    SetupKafka.run()
    sleep(5)
    SetupMemgraph.run()
    logging.basicConfig(filename="/usr/src/appcore/Log/log.txt", # This needs to be a constant
                        level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.getLogger("kafka").setLevel(logging.WARNING)
    logging.info("Core is ready")
    CoreKafkaConsumer.run()


if __name__ == "__main__":
    setup()