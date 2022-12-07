from gqlalchemy import Node, Field, Relationship
from backend.server.server import memgraph
from typing import List


class User(Node, db=memgraph):
    username: str = Field(index=True, unique=True, exist=True, db=memgraph)


class Repo(Node, db=memgraph):
    repo_id: int = Field(index=True, unique=True, exist=True, db=memgraph)
    name: str = Field(index=True, exist=True, db=memgraph)
    full_name: str = Field(unique=True, index=True, exist=True, db=memgraph)
    public: bool = Field(exist=True, db=memgraph)
    updated_at: int = Field(exist=True, db=memgraph)
    languages: List[str] = Field(exist=True, db=memgraph)
    github_url: str = Field(exist=True, db=memgraph)
    default_branch: str = Field(exist=True, db=memgraph)


class UserRepo(Relationship, db=memgraph, type="HAS_REPO"):
    is_starred: bool = Field(exist=True, db=memgraph)


class Branch(Node, db=memgraph):
    name: str = Field(index=True, exist=True, db=memgraph)
    commit_id: str = Field(index=True, exist=True, db=memgraph)


class BranchRepo(Relationship, db=memgraph, type="HAS_BRANCH"):
    pass


class Commit(Node, db=memgraph):
    commit_id: str = Field(index=True, unique=True, exist=True, db=memgraph)
    message: str = Field(exist=True, db=memgraph)
    timestamp: int = Field(exist=True, db=memgraph)


class CommitBranch(Relationship, db=memgraph, type="HAS_COMMIT"):
    pass


class Status(Node, db=memgraph):
    status: str = Field(exist=True, db=memgraph)


class StatusCommit(Relationship, db=memgraph, type="HAS_STATUS"):
    pass


class File(Node, db=memgraph):
    file_hash: str = Field(index=True, unique=True, exist=True, db=memgraph)


class Dir(Node, db=memgraph):
    name: str = Field(exist=True, db=memgraph)
    path: str = Field(exist=True, index=True, db=memgraph)


class IsParentOf(Relationship, db=memgraph, type="IS_PARENT_OF"):
    pass


class HasFile(Relationship, db=memgraph, type="HAS_FILE"):
    name: str = Field(exist=True, db=memgraph)
    path: str = Field(exist=True, unique=True, index=True, db=memgraph)


class RootFolderCommit(Relationship, db=memgraph, type="TO_ROOT_FOLDER"):
    pass


class DependsOn(Relationship, db=memgraph, type="DEPENDS_ON"):
    number_of_calls: int = Field(exist=True, db=memgraph)

