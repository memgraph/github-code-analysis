from enum import Enum
from typing import Dict
from appcore.KafkaClient.QueryResponseImpls.AllRepositoryInformation import AllRepositoryInformation


class QueryResponseImplsList(Enum):
    """
    This class is used to list all the implementations of the QueryResponse interface.
    """
    QUERY_RESPONSES: Dict = {
        "all_repository_information": AllRepositoryInformation,
    }
