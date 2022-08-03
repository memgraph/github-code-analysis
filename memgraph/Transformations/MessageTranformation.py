import mgp
from json import loads as json_loads
from typing import List, Dict
from enum import Enum
from abc import ABC, abstractmethod


class KafkaMessageResponse(ABC):
    @staticmethod
    @abstractmethod
    def get_response(data: Dict) -> str:
        pass


class FiletreeKafkaMessageResponse(KafkaMessageResponse):
    @staticmethod
    def get_response(data: Dict) -> str:
        merge_node_format = "MERGE ({id}:{type} {{name: '{name}', path: '{path}'}})"
        merge_edge_format = "MERGE ({id1})-[:IsParentOf]->({id2})"

        commands = []
        for node_before in data["before"]:
            commands.append(merge_node_format.format(id=node_before["id"], type="Dir", name=node_before["data"]["name"], path=node_before["data"]["path"]))
        
        for before_edge in data["link_before"]:
            commands.append(merge_edge_format.format(id1=before_edge["source"], id2=before_edge["target"]))
        
        if data["after"] != {}:
            commands.append(merge_node_format.format(id=data["after"]["id"], type="File", name=data["after"]["data"]["name"], path=data["after"]["data"]["path"]))
        
        if data["link_after"] != {}:
            commands.append(merge_edge_format.format(id1=data["link_after"]["source"], id2=data["link_after"]["target"]))

        return '\n'.join(commands)


class KafkaMessageResponseDict(Enum):
    response_dict: Dict[str, KafkaMessageResponse] = {
        "filetree": FiletreeKafkaMessageResponse,
    }


@mgp.transformation
def transform_data(messages: mgp.Messages) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    queries: List[mg.Record] = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        data = json_loads(message.payload().decode("utf8"))
        if KafkaMessageResponseDict.response_dict.value.get(data["type"]) is None:
            return queries
            
        queries.append(
                mgp.Record(
                    query=KafkaMessageResponseDict.response_dict.value.get(data["type"]).get_response(data["data"]),
                    parameters=None,
                )
        )

    return queries
