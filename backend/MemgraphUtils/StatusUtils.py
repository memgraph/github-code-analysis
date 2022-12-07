from datetime import datetime
from typing import List, Dict, Optional

from gqlalchemy import Memgraph, Match
from gqlalchemy.query_builders.memgraph_query_builder import Operator

from backend.MemgraphUtils.Models import Status


class StatusUtils:
    def __init__(self, memgraph_instance: Memgraph):
        self._memgraph_instance = memgraph_instance

    def get_commit_status(self, commit_id: str) -> Optional[str]:
        status = list(
            Match()
            .node(labels="Commit", variable="c")
            .to(relationship_type="HAS_STATUS", variable="relationship")
            .node(labels="Status", variable="s")
            .where(item="c.commit_id", operator=Operator.EQUAL, expression=f"'{commit_id}'")
            .return_(results=("s", "status"))
            .execute()
        )

        if len(status) == 0:
            return None

        return status[0].get("status").status

    def add_status_to_commit(self, commit_id: str, status: str) -> None:
        status_node = Status(status=status).save(self._memgraph_instance)
        self._memgraph_instance.execute(
            f"""MATCH (start_node:Commit), (end_node:Status) WHERE start_node.commit_id = "{commit_id}" AND id(end_node) = {status_node._id} MERGE (start_node)-[relationship:HAS_STATUS]->(end_node) RETURN relationship"""
        )




