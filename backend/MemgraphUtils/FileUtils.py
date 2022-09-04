from gqlalchemy import Memgraph, Match
from gqlalchemy.query_builders.memgraph_query_builder import Operator, Order
from gqlalchemy.graph_algorithms.integrated_algorithms import BreadthFirstSearch
from typing import List, Dict, Optional
from mgclient import Node
from random import choice
from backend.MemgraphUtils.Models import File


class FileUtils:
    def __init__(self, memgraph_instance: Memgraph):
        self._memgraph_instance = memgraph_instance

    def get_filetree_for_commit(self, commit_id: str) -> Optional[List[Dict]]:
        graph_results = []

        results = list(
            Match()
            .add_custom_cypher("(c:Commit)-[:TO_ROOT_FOLDER]->(dir:Dir)-[r:IS_PARENT_OF |:HAS_FILE *]->(d)")
            .where(item="c.commit_id", operator=Operator.EQUAL,
                   expression=f"'{commit_id}'")
            .return_(results=[("dir", "dir"), ("d", "d"), ("r[-1]", "r")])
            .execute()
        )

        if len(results) == 0:
            return None

        graph_results.append({"name": results[0].get("dir").name, "path": results[0].get("dir").path, "label": "Dir"})

        for result in results:
            if type(result.get("d")) == File:
                graph_results.append({"name": result.get("r").name, "path": result.get("r").path, "label": "File"})
            else:
                graph_results.append({"name": result.get("d").name, "path": result.get("d").path, "label": "Dir"})

        return graph_results

    def get_dependencies(self, commit_id: str) -> Optional[Dict]:
        root_filename_results = list(
            Match()
            .node(labels="Commit", variable="c")
            .to(relationship_type="TO_ROOT_FOLDER", variable="relationship")
            .node(labels="Dir", variable="d")
            .where(item="c.commit_id", operator=Operator.EQUAL,
                     expression=f"'{commit_id}'")
            .return_(results=("d.name", "root_dir_name"))
            .execute()
        )

        if len(root_filename_results) == 0:
            return None

        root_filename = root_filename_results[0].get("root_dir_name")
        nodes = {}
        edges = []

        results = list(
            Match()
            .node(labels="Dir", variable="d1")
            .to(relationship_type="HAS_FILE", variable="f1")
            .node(labels="File", variable="file1")
            .to(relationship_type="DEPENDS_ON", variable="depends", directed=False)
            .node(labels="File", variable="file2")
            .match()
            .node(labels="Dir", variable="d2")
            .to(relationship_type="HAS_FILE", variable="f2")
            .node(variable="file2")
            .add_custom_cypher(f' WHERE contains(d1.path, "{root_filename}") AND contains(d2.path, "{root_filename}")')
            .return_(results=[("f1", "f1"), ("f2", "f2"), ("depends", "depends")])
            .execute()
        )

        if len(results) == 0:
            return None

        pagerank_results = list(
            Match()
            .node(labels="Dir", variable="d1")
            .to(relationship_type="HAS_FILE", variable="f1")
            .node(labels="File", variable="file1")
            .to(relationship_type="DEPENDS_ON", variable="depends", directed=False)
            .node(labels="File", variable="file2")
            .add_custom_cypher(f' WHERE contains(d1.path, "{root_filename}")')
            .with_(results=[("COLLECT(file2)", "nodes"), ("COLLECT(depends)", "edges")])
            .add_custom_cypher(" CALL pagerank.get_subgraph(nodes, edges, 1000)")
            .yield_(results=[("node", "node"), ("rank", "rank")])
            .return_(results=[("node", "node"), ("rank", "rank")])
            .execute()
        )

        ranks = {}

        for pagerank_result in pagerank_results:
            ranks[pagerank_result.get("node")._id] = pagerank_result.get("rank")

        community_detection_results = (
            Match()
            .node(labels="Dir", variable="d1")
            .to(relationship_type="HAS_FILE", variable="f1")
            .node(labels="File", variable="file1")
            .to(relationship_type="DEPENDS_ON", variable="depends", directed=False)
            .node(labels="File", variable="file2")
            .add_custom_cypher(f' WHERE contains(d1.path, "{root_filename}")')
            .with_(results=[("COLLECT(file2)", "nodes"), ("COLLECT(depends)", "edges")])
            .add_custom_cypher(" CALL community_detection.get_subgraph(nodes, edges)")
            .yield_(results=[("node", "node"), ("community_id", "community_id")])
            .return_(results=[("node", "node"), ("community_id", "community_id")])
            .execute()
        )

        node_communities = {}
        community_colors = {}

        for community_detection_result in community_detection_results:
            node_communities[community_detection_result.get("node")._id] = community_detection_result.get("community_id")
            community_colors[community_detection_result.get("community_id")] = "#"+''.join([choice('0123456789ABCDEF') for i in range(6)])

        for relationships in results:
            if relationships.get("f1")._end_node_id not in nodes:
                nodes[relationships.get("f1")._end_node_id] = {"id": relationships.get("f1")._end_node_id, "name": relationships.get("f1").name, "path": relationships.get("f1").path, "size": 15 + ranks.get(relationships.get("f1")._end_node_id, 0.1) * 300, "color": community_colors.get(node_communities.get(relationships.get("f1")._end_node_id), "#000000")}

            if relationships.get("f2")._end_node_id not in nodes:
                nodes[relationships.get("f2")._end_node_id] = {"id": relationships.get("f2")._end_node_id, "name": relationships.get("f2").name, "path": relationships.get("f2").path, "size": 10 + ranks.get(relationships.get("f2")._end_node_id, 0.05) * 300, "color": community_colors.get(node_communities.get(relationships.get("f2")._end_node_id), "#000000")}

            edges.append({"source": relationships.get("depends")._start_node_id, "target": relationships.get("depends")._end_node_id})

        return {"nodes": list(nodes.values()), "links": edges, "nodes_dict": nodes}