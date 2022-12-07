from enum import Enum


class MemgraphConstants(Enum):
    MEMGRAPH_HOST: str = "memgraph"
    MEMGRAPH_PORT: int = 7687
    MEMGRAPH_USER: str = ""
    MEMGRAPH_PASSWORD: str = ""
