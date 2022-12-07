from gqlalchemy import Memgraph
from backend.MemgraphUtils.MemgraphConstants import MemgraphConstants


class MemgraphInstance:
    @staticmethod
    def get_instance() -> Memgraph:
        return Memgraph(host=MemgraphConstants.MEMGRAPH_HOST.value, port=MemgraphConstants.MEMGRAPH_PORT.value)
