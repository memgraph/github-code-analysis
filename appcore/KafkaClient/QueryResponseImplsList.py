from enum import Enum
from appcore.KafkaClient.QueryResponseImpls.DownloadAndGenEverything import DownloadAndGenEverything


class QueryResponseImplsList(Enum):
    """
    This class is used to list all the implementations of the QueryResponse interface.
    """
    QUERY_RESPONSES: dict = {
        "download_and_get_all": DownloadAndGenEverything,
    }
