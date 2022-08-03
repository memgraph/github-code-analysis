from json import loads as json_loads
from appcore.KafkaClient.QueryResponseImplsList import QueryResponseImplsList
import logging


class QueryParsing:
    @staticmethod
    def recognize(query: str) -> None:
        data = json_loads(query)
        query_type = data.get("query_type")
        query_response_impl = QueryResponseImplsList.QUERY_RESPONSES.value.get(query_type)
        if query_response_impl:
            query_response_impl.query_response(data)
        else:
            logging.error(f"Query type {query_type} is not recognized.")
