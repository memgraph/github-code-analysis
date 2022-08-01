from gqlalchemy import Memgraph
from gqlalchemy.exceptions import GQLAlchemyDatabaseError


class SetupMemgraph:
    @staticmethod
    def run():
        memgraph = Memgraph(host="memgraph", port=7687)
        query = '''CREATE KAFKA STREAM `gitstream` TOPICS `to_memgraph_data` TRANSFORM MessageTransformation.transform_data BATCH_INTERVAL 100 BATCH_SIZE 1000 CONSUMER_GROUP `mg_consumer` BOOTSTRAP_SERVERS "broker:9092"'''
        try:
            memgraph.execute(query)
        except GQLAlchemyDatabaseError:
            pass

        memgraph.execute('''STOP ALL STREAMS''')
        
        memgraph.execute('''CALL mg.kafka_set_stream_offset("gitstream", -2)''')

        try:
            memgraph.execute('START STREAM `gitstream`')
        except GQLAlchemyDatabaseError:
            pass
