import mgp
from json import loads as json_loads
from typing import List, Dict, Generator
from enum import Enum
from abc import ABC, abstractmethod


class KafkaMessageResponse(ABC):
    @staticmethod
    @abstractmethod
    def get_response(data: Dict) -> Generator[str, None, None]:
        pass


class FiletreeKafkaMessageResponse(KafkaMessageResponse):
    @staticmethod
    def get_response(data: Dict) -> Generator[str, None, None]:
        create_node_format = """CREATE ({id}:{type} {{name: "{name}", path: '{path}'}})"""
        create_edge_format = """MATCH (dir1:Dir {{path: "{source_path}"}}), (dir2:Dir {{path: "{target_path}"}}) CREATE (dir1)-[:IS_PARENT_OF]->(dir2)"""
        merge_file_format = """MERGE ({id}:{type} {{file_hash: '{file_hash}'}})"""
        create_file_edge_format = """MATCH (dir:Dir {{path: "{path}"}}) {merge_node} CREATE (dir)-[:HAS_FILE {{name: "{name}", path: "{file_path}"}}]->({id2})"""

        for node_before in data["before"]:
            yield create_node_format.format(
                id=node_before["id"], type="Dir", name=node_before["data"]["name"], path=node_before["data"]["path"]
            )

        for before_edge in data["link_before"]:
            yield create_edge_format.format(source_path=before_edge["source"], target_path=before_edge["target"])

        if data["after"] != {}:
            merge_node = merge_file_format.format(
                id=data["after"]["id"], type="File", file_hash=data["after"]["data"]["file_hash"]
            )
            if data["link_after"] != {}:
                yield (
                    create_file_edge_format.format(
                        path=data["link_after"]["source"],
                        id2=data["link_after"]["target"],
                        name=data["after"]["data"]["name"],
                        file_path=data["after"]["data"]["path"],
                        merge_node=merge_node,
                    )
                )


class ConnectCommitToRootFileKafkaMessageResponse(KafkaMessageResponse):
    @staticmethod
    def get_response(data: Dict) -> Generator[str, None, None]:
        yield f"""MATCH (c:Commit {{commit_id: '{data["commit_sha"]}'}}), (d:Dir {{path: "{data["extracted_file"].replace("/", "")}"}}) MERGE (c)-[:TO_ROOT_FOLDER]-(d)"""


class UpdateStatusToReadyKafkaMessageResponse(KafkaMessageResponse):
    @staticmethod
    def get_response(data: Dict) -> Generator[str, None, None]:
        yield f"""MATCH (c:Commit {{commit_id: "{data["commit_sha"]}"}})-[:HAS_STATUS]-(s:Status) SET s.status = 'ready'"""


class CreateDependencyKafkaMessageResponse(KafkaMessageResponse):
    @staticmethod
    def get_response(data: Dict) -> Generator[str, None, None]:
        for imports, value in data.get("imports").items():
            if type(value) == dict:
                number_of_calls = sum(data.get("imports")[imports].values())
            else:
                number_of_calls = data.get("imports")[imports]

            yield f"""MATCH (:Dir)-[r1:HAS_FILE]-(f1:File), (:Dir)-[r2:HAS_FILE]-(f2:File) WHERE r1.path = "{data["filename"]}" AND contains(r2.path, "{data["root_path"]}") AND contains(r2.path, "{imports}") MERGE (f1)-[:DEPENDS_ON {{number_of_calls: {number_of_calls}}}]-(f2)"""


class KafkaMessageResponseDict(Enum):
    response_dict: Dict[str, KafkaMessageResponse] = {
        "filetree": FiletreeKafkaMessageResponse,
        "connect_commit_file": ConnectCommitToRootFileKafkaMessageResponse,
        "update_status_to_ready": UpdateStatusToReadyKafkaMessageResponse,
        "imports_dependency": CreateDependencyKafkaMessageResponse,
    }


@mgp.transformation
def transform_data(messages: mgp.Messages) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    queries: List[mg.Record] = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        data = json_loads(message.payload().decode("utf8"))
        if KafkaMessageResponseDict.response_dict.value.get(data["type"]) is None:
            return queries

        for query in KafkaMessageResponseDict.response_dict.value.get(data["type"]).get_response(data["data"]):
            if query:
                queries.append(
                    mgp.Record(
                        query=query,
                        parameters=None,
                    )
                )

    return queries
