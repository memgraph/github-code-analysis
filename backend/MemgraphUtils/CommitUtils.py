from datetime import datetime
from typing import List, Dict, Optional

from gqlalchemy import Memgraph, Match
from gqlalchemy.query_builders.memgraph_query_builder import Operator, Order

from backend.MemgraphUtils.Models import Commit


class CommitUtils:
    def __init__(self, memgraph_instance: Memgraph) -> None:
        self._memgraph_instance = memgraph_instance

    def map_commit_object_to_json(self, commit: Commit) -> Dict:
        return {
            "commit_id": commit.commit_id,
            "message": commit.message,
            "timestamp": commit.timestamp,
        }

    def get_commits_for_branch(self, user_repo: str, branch_name: str) -> List[Dict]:
        return list(
            Match()
            .node(labels="Repo", variable="r")
            .to(relationship_type="HAS_BRANCH", variable="relationship1")
            .node(labels="Branch", variable="b")
            .to(relationship_type="HAS_COMMIT", variable="relationship2")
            .node(labels="Commit", variable="c")
            .where(item="r.full_name", operator=Operator.EQUAL, expression=f"'{user_repo}'")
            .and_where(item="b.name", operator=Operator.EQUAL, expression=f"'{branch_name}'")
            .return_(results=[("c", "commit"), ("b", "branch")])
            .order_by(properties=("c.timestamp", Order.DESC))
            .execute()
        )

    def save_commits(self, user_repo: str, branch_name: str, commit_list: List[Dict]) -> None:
        for commit in commit_list:
            commit_node = self._memgraph_instance.save_node(
                Commit(commit_id=commit.get("sha"), message=commit.get("commit").get("message"),
                       timestamp=datetime.strptime(commit.get("commit").get("author").get("date"),
                                                   "%Y-%m-%dT%H:%M:%SZ").timestamp()))
            self._memgraph_instance.execute(
                f"""MATCH (repo:Repo)-[]-(start_node:Branch), (end_node:Commit) WHERE repo.full_name = "{user_repo}" AND start_node.name = "{branch_name}" AND id(end_node) = {commit_node._id} MERGE (start_node)-[relationship:HAS_COMMIT]->(end_node) RETURN relationship"""
            )

    def get_commit(self, branch_name: str, commit_id: str) -> Optional[Commit]:
        commits = list(Match()
                       .node(labels="Branch", variable="b")
                       .to(relationship_type="HAS_COMMIT", variable="relationship")
                       .node(labels="Commit", variable="c")
                       .where(item="c.commit_id", operator=Operator.EQUAL, expression=f"'{commit_id}'")
                       .and_where(item="b.name", operator=Operator.EQUAL, expression=f"'{branch_name}'")
                       .return_(results=("c", "commit"))
                       .execute()
                       )

        if len(commits) == 0:
            return None

        return commits[0].get("commit")
