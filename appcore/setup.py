from appcore.Config.SetupKafka import SetupKafka
from appcore.Config.SetupMemgraph import SetupMemgraph
from appcore.KafkaClient.CoreKafkaConsumer import CoreKafkaConsumer
from time import sleep
import logging


def setup():
    sleep(4)
    SetupKafka.run()
    sleep(10)
    SetupMemgraph.run()
    sleep(2)
    logging.basicConfig(filename="/usr/src/appcore/Log/logfile.txt", # This needs to be a constant
                        level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.info("Core is ready")
    CoreKafkaConsumer.run()


if __name__ == "__main__":
    setup()