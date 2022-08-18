from gqlalchemy import Node, Field, Relationship
from backend.server.server import memgraph
from typing import List


class User(Node, index=True, db=memgraph):
    username: str = Field(index=True, unique=True, exist=True, db=memgraph)


class Repo(Node, index=True, db=memgraph):
    repo_id: int = Field(index=True, unique=True, exist=True, db=memgraph)
    name: str = Field(index=True, exist=True, db=memgraph)
    full_name: str = Field(unique=True, index=True, exist=True, db=memgraph)
    public: bool = Field(exist=True, db=memgraph)
    updated_at: int = Field(exist=True, db=memgraph)
    languages: List[str] = Field(exist=True, db=memgraph)
    github_url: str = Field(exist=True, db=memgraph)


class RepoUser(Relationship, db=memgraph, type="HAS_REPO"):
    is_starred: bool = Field(exist=True, db=memgraph)
