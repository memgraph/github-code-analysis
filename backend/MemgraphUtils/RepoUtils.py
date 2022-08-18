from datetime import datetime
from typing import List, Dict

from gqlalchemy import Memgraph, Match
from gqlalchemy.query_builders.memgraph_query_builder import Operator, Order

from backend.MemgraphUtils.Models import Repo, User


class RepoUtils:
    def __init__(self, memgraph_instance: Memgraph) -> None:
        self._memgraph_instance = memgraph_instance

    def map_to_repo_object(self, repo_dict: Dict) -> Repo:
        return Repo(
            repo_id=repo_dict.get("id"),
            name=repo_dict.get("name"),
            full_name=repo_dict.get("full_name"),
            public=repo_dict.get("public"),
            updated_at=repo_dict.get("updated_at"),
            languages=repo_dict.get("languages"),
            github_url=repo_dict.get("github_url"),
        )

    def map_repo_object_to_json(self, repo_node: Repo, is_starred=False) -> Dict:
        return {
            "repo_id": repo_node.repo_id,
            "name": repo_node.name,
            "full_name": repo_node.full_name,
            "public": repo_node.public,
            "updated_at": datetime.fromtimestamp(repo_node.updated_at).strftime("%d %b, %Y"),
            "languages": repo_node.languages,
            "github_url": repo_node.github_url,
            "is_starred": is_starred,
        }

    def get_repositories(self, username: str, all=True, is_starred=False) -> List[Dict]:
        if all:
            return list(
                Match()
                .node(labels="User", variable="u")
                .to(relationship_type="HAS_REPO", variable="relationship")
                .node(labels="Repo", variable="r")
                .where(item="u.username", operator=Operator.EQUAL, expression=f"'{username}'")
                .return_({"r": "repository", "relationship": "edge"})
                .order_by(properties=("r.updated_at", Order.DESC))
                .execute()
            )

        return list(
            Match()
            .node(labels="User", variable="u")
            .to(relationship_type="HAS_REPO", variable="relationship")
            .node(labels="Repo", variable="r")
            .where(item="u.username", operator=Operator.EQUAL, expression=f"'{username}'")
            .and_where(item="relationship.is_starred", operator=Operator.EQUAL, expression=f"{is_starred}")
            .return_({"r": "repository"})
            .order_by(properties=("r.updated_at", Order.DESC))
            .execute()
        )

    def save_repositories(self, username: str, repo_list: List[Dict]) -> None:
        if len(repo_list) == 0:
            return

        user_node = User(username=username).load(self._memgraph_instance)
        for repo in repo_list:
            repo_node = Repo(
                repo_id=repo.get("id"),
                name=repo.get("name"),
                full_name=repo.get("full_name"),
                public=repo.get("public"),
                updated_at=repo.get("updated_at").timestamp(),
                languages=repo.get("languages"),
                github_url=repo.get("github_url"),
            )
            repo_node = self._memgraph_instance.save_node(repo_node)
            self._memgraph_instance.execute(
                f"""MATCH (start_node), (end_node) WHERE id(start_node) = {user_node._id} AND id(end_node) = {repo_node._id} MERGE (start_node)-[relationship:HAS_REPO {{is_starred: {repo.get("is_starred")}}}]->(end_node) RETURN relationship"""
            )  # In GQLAlchemy edges are created using the command CREATE

    def repo_needs_updating(self, repo_dict: Dict, memgraph_repo: Repo) -> bool:
        if (
            memgraph_repo.updated_at
            != int(datetime.strptime(repo_dict.get("pushed_at"), "%Y-%m-%dT%H:%M:%SZ").timestamp())
            or memgraph_repo.name != repo_dict.get("name")
            or memgraph_repo.full_name != repo_dict.get("full_name")
            or memgraph_repo.public != (repo_dict.get("visibility", "public") == "public")
        ):
            print(repo_dict.get("full_name"), memgraph_repo.full_name)
            return True
        return False

    def delete_repositories(self, username: str) -> None:
        (
            Match()
            .node(labels="User", variable="u")
            .to(relationship_type="HAS_REPO", variable="relationship")
            .node(labels="Repo", variable="r")
            .where(item="u.username", operator=Operator.EQUAL, expression=f"'{username}'")
            .delete(variable_expressions="r", detach=True)
            .execute()
        )

    def update_repositories(self, repo_list: List[Dict]) -> None:
        for repo in repo_list:
            repo_id = repo.get("id")
            repo_full_name = repo.get("full_name")
            repo_name = repo.get("name")
            repo_updated_at = int(repo.get("updated_at").timestamp())
            repo_languages = repo.get("languages")
            repo_github_url = repo.get("github_url")
            repo_is_public = repo.get("public")
            self._memgraph_instance.execute(
                Match()  # Execute doesn't work, it doesn't send query to memgraph
                .node(labels="Repo", variable="r")
                .where(item="r.repo_id", operator=Operator.EQUAL, literal=repo_id)
                .set_(
                    item="r",
                    operator=Operator.ASSIGNMENT,
                    literal={
                        "repo_id": repo_id,
                        "name": repo_name,
                        "full_name": repo_full_name,
                        "updated_at": repo_updated_at,
                        "languages": repo_languages,
                        "github_url": repo_github_url,
                        "public": repo_is_public,
                    },
                )
                .return_()
                .construct_query()
            )

    def detach_repositories(self, username: str, repo_list: List[Repo]) -> None:
        for repo in repo_list:
            self._memgraph_instance.execute(
                Match()
                .node(labels="User", variable="u")
                .to(relationship_type="HAS_REPO", variable="relationship")
                .node(labels="Repo", variable="r")
                .where(item="u.username", operator=Operator.EQUAL, expression=f"'{username}'")
                .and_where(item="r.repo_id", operator=Operator.EQUAL, literal=repo.repo_id)
                .delete(variable_expressions="relationship")
                .return_()
                .construct_query()
            )  # Execute doesn't send the query to Memgraph

    def update_edges(self, username: str, repo_id_list: List[Dict]) -> None:
        for repo_id_edge_info in repo_id_list:
            self._memgraph_instance.execute(
                Match()
                .node(labels="User", variable="u")
                .to(relationship_type="HAS_REPO", variable="relationship")
                .node(labels="Repo", variable="r")
                .where(item="u.username", operator=Operator.EQUAL, expression=f"'{username}'")
                .and_where(item="r.repo_id", operator=Operator.EQUAL, expression=f"{repo_id_edge_info.get('repo_id')}")
                .set_(
                    item="relationship",
                    operator=Operator.ASSIGNMENT,
                    literal={"is_starred": repo_id_edge_info.get("is_starred")},
                )
                .return_()
                .construct_query()
            )

    @staticmethod
    def remove_unattached_repositories():
        pass
