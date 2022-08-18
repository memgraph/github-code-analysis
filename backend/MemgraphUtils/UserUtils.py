from gqlalchemy import Memgraph
from gqlalchemy.exceptions import GQLAlchemyError

from backend.MemgraphUtils.Models import User


class UserUtils:
    def __init__(self, memgraph_instance: Memgraph) -> None:
        self._memgraph_instance = memgraph_instance

    def user_exists(self, username: str) -> bool:
        try:
            user = User(username=username).load(self._memgraph_instance)
            return user is not None
        except GQLAlchemyError:
            return False

    def save_user(
        self,
        username: str,
    ) -> None:
        user = User(username=username)
        self._memgraph_instance.save_node(user)
