from gqlalchemy import Memgraph, Match, Merge
from gqlalchemy.query_builders.memgraph_query_builder import Operator, Order
from typing import List, Dict, Optional
from backend.MemgraphUtils.Models import Branch


class BranchUtils:
    def __init__(self, memgraph_instance: Memgraph) -> None:
        self._memgraph_instance = memgraph_instance

    def map_branch_object_to_json(self, branch: Branch):
        return {
            "name": branch.name,
            "commit_id": branch.commit_id,
        }

    def get_branches_for_repo(self, user_repo: str) -> List[Dict]:
        return list(
            Match()
            .node(labels="Repo", variable="r")
            .to(relationship_type="HAS_BRANCH", variable="relationship")
            .node(labels="Branch", variable="b")
            .where(item="r.full_name", operator=Operator.EQUAL, expression=f"'{user_repo}'")
            .return_(results=[("b", "branch"), ("r.default_branch", "default_branch_for_repo")])
            .execute()
        )

    def save_branches(self, user_repo: str, branch_list: List[Dict]):
        for branch in branch_list:
            branch_node = self._memgraph_instance.save_node(
                Branch(name=branch.get("name"), commit_id=branch.get("commit").get("sha")))
            self._memgraph_instance.execute(
                f"""MATCH (start_node:Repo), (end_node) WHERE start_node.full_name = "{user_repo}" AND id(end_node) = {branch_node._id} MERGE (start_node)-[relationship:HAS_BRANCH]->(end_node) RETURN relationship"""
            )

    def delete_branches(self, user_repo: str, branch_list: List[str]):
        for branch in branch_list:
            (
                Match()
                .node(labels="Repo", variable="r")
                .to(relationship_type="HAS_BRANCH", variable="relationship")
                .node(labels="Branch", variable="b")
                .where(item="r.full_name", operator=Operator.EQUAL, expression=f"'{user_repo}'")
                .and_where(item="b.name", operator=Operator.EQUAL, expression=f"'{branch}'")
                .delete(variable_expressions="r", detach=True)
                .execute()
            )

    def branch_needs_updating(self, git_branch_data: Dict, memgraph_branch_data: Branch):
        return git_branch_data.get("commit").get("sha") != memgraph_branch_data.commit_id

    def update_branch(self, user_repo: str, branch_data: Dict):
        (
            Match()
            .node(labels="Repo", variable="r")
            .to(relationship_type="HAS_BRANCH", variable="relationship")
            .node(labels="Branch", variable="b")
            .where(item="r.full_name", operator=Operator.EQUAL, expression=f"'{user_repo}'")
            .and_where(item="b.name", operator=Operator.EQUAL, expression=f"'{branch_data.get('name')}'")
            .set_(item="b.commit_id", operator=Operator.ASSIGNMENT,
                  expression=f"'{branch_data.get('commit').get('sha')}'")
            .return_()
            .execute()
        )

    def get_branch(self, user_repo: str, branch_name: str) -> Optional[Branch]:
        branch_data = list(
                Match()
                .node(labels="Repo", variable="r")
                .to(relationship_type="HAS_BRANCH", variable="relationship")
                .node(labels="Branch", variable="b")
                .where(item="r.full_name", operator=Operator.EQUAL, expression=f"'{user_repo}'")
                .and_where(item="b.name", operator=Operator.EQUAL, expression=f"'{branch_name}'")
                .return_(results=("b", "branch"))
                .execute()
            )
        if len(branch_data) == 1:
            return branch_data[0].get("branch")
        return None

    def branch_exists(self, user_repo: str, branch_name: str) -> bool:
        return self.get_branch(user_repo=user_repo, branch_name=branch_name) is not None
