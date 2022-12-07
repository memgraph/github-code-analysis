import type { NextPage } from "next";
import { Button, Grid, Typography, Box, Stack } from "@mui/material";
import NetworkGraph from "../comps/NetworkGraph";
import Link from "next/link";
import {GitHub} from "@mui/icons-material";


const graph_data = {'nodes': [{'id': 35532, 'name': 'models.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/models.py', 'size':
            32.300657744226726, 'color': '#FB6E00'}, {'id': 35488, 'name': '__init__.py', 'path':
            'memgraph-gqlalchemy-7fbec93/gqlalchemy/__init__.py', 'size': 11.90260223043564, 'color': '#FFC500'}, {'id': 35490,
        'name': 'disk_storage.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/disk_storage.py', 'size': 18.11416059218413,
        'color': '#FFC500'}, {'id': 35530, 'name': 'instance_runner.py', 'path':
            'memgraph-gqlalchemy-7fbec93/gqlalchemy/instance_runner.py', 'size': 19.452820989308023, 'color': '#FFC500'}, {'id':
            35491, 'name': 'exceptions.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/exceptions.py', 'size':
            36.02661889114847, 'color': '#FB6E00'}, {'id': 35534, 'name': 'declarative_base.py', 'path':
            'memgraph-gqlalchemy-7fbec93/gqlalchemy/query_builders/declarative_base.py', 'size': 19.627544147868136, 'color':
            '#FFC500'}, {'id': 35535, 'name': 'memgraph_query_builder.py', 'path':
            'memgraph-gqlalchemy-7fbec93/gqlalchemy/query_builders/memgraph_query_builder.py', 'size': 21.375955468813782, 'color':
            '#FFC500'}, {'id': 35536, 'name': 'neo4j_query_builder.py', 'path':
            'memgraph-gqlalchemy-7fbec93/gqlalchemy/query_builders/neo4j_query_builder.py', 'size': 17.431306119470158, 'color':
            '#FFC500'}, {'id': 35545, 'name': 'memgraph.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/vendors/memgraph.py',
        'size': 25.23207008641456, 'color': '#FFC500'}, {'id': 35546, 'name': 'neo4j.py', 'path':
            'memgraph-gqlalchemy-7fbec93/gqlalchemy/vendors/neo4j.py', 'size': 21.106827473177553, 'color': '#FB6E00'}, {'id':
            35544, 'name': 'database_client.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/vendors/database_client.py',
        'size': 21.905794856008217, 'color': '#FB6E00'}, {'id': 35489, 'name': 'connection.py', 'path':
            'memgraph-gqlalchemy-7fbec93/gqlalchemy/connection.py', 'size': 15.029286781758984, 'color': '#FB6E00'}, {'id': 35566,
        'name': 'test_index.py', 'path': 'memgraph-gqlalchemy-7fbec93/tests/integration/test_index.py', 'size':
            16.90260223043564, 'color': '#FB6E00'}, {'id': 35569, 'name': 'test_stream.py', 'path':
            'memgraph-gqlalchemy-7fbec93/tests/integration/test_stream.py', 'size': 16.90260223043564, 'color': '#FB6E00'}, {'id':
            35574, 'name': 'test_add_query_modules.py', 'path':
            'memgraph-gqlalchemy-7fbec93/tests/memgraph/test_add_query_modules.py', 'size': 16.90260223043564, 'color': '#FB6E00'},
        {'id': 35592, 'name': 'test_query_builders.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/query_builders/test_query_builders.py', 'size': 16.90260223043564, 'color':
                '#FB6E00'}, {'id': 35593, 'name': 'test_instance_runner.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/test_instance_runner.py', 'size': 16.90260223043564, 'color': '#FFC500'}, {'id':
                35553, 'name': 'conftest.py', 'path': 'memgraph-gqlalchemy-7fbec93/tests/conftest.py', 'size': 16.90260223043564,
            'color': '#FFC500'}, {'id': 35474, 'name': 'test_loaders.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/loaders/test_loaders.py', 'size': 16.90260223043564, 'color': '#868089'}, {'id':
                35531, 'name': 'loaders.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/loaders.py', 'size': 12.172137546414021,
            'color': '#868089'}, {'id': 35541, 'name': 'transformations.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/transformations.py', 'size': 18.25027881032755, 'color': '#F9AF73'}, {'id':
                35568, 'name': 'test_networkx.py', 'path': 'memgraph-gqlalchemy-7fbec93/tests/integration/test_networkx.py', 'size':
                16.90260223043564, 'color': '#F9AF73'}, {'id': 35570, 'name': 'test_trigger.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/integration/test_trigger.py', 'size': 16.90260223043564, 'color': '#FB6E00'}, {'id':
                35577, 'name': 'test_automatic_deserialisation.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/ogm/test_automatic_deserialisation.py', 'size': 16.90260223043564, 'color':
                '#FB6E00'}, {'id': 35598, 'name': 'test_transformations.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/test_transformations.py', 'size': 16.90260223043564, 'color': '#F9AF73'}, {'id':
                35542, 'name': 'utilities.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/utilities.py', 'size': 24.42847438533373,
            'color': '#F9AF73'}, {'id': 35590, 'name': 'test_memgraph_query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/query_builders/test_memgraph_query_builder.py', 'size': 16.90260223043564, 'color':
                '#F9AF73'}, {'id': 35591, 'name': 'test_neo4j_query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/query_builders/test_neo4j_query_builder.py', 'size': 16.90260223043564, 'color':
                '#F9AF73'}, {'id': 35599, 'name': 'test_utilities.py', 'path': 'memgraph-gqlalchemy-7fbec93/tests/test_utilities.py',
            'size': 16.90260223043564, 'color': '#F9AF73'}, {'id': 35398, 'name': 'integrated_algorithms.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/graph_algorithms/integrated_algorithms.py', 'size': 38.89566258187239, 'color':
                '#DC2223'}, {'id': 35559, 'name': 'test_query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/graph_algorithms/test_query_builder.py', 'size': 16.90260223043564, 'color':
                '#FFC500'}, {'id': 35529, 'name': 'query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/graph_algorithms/query_builder.py', 'size': 12.711208178370786, 'color':
                '#FFC500'}, {'id': 35399, 'name': 'query_modules.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/graph_algorithms/query_modules.py', 'size': 36.54714629362779, 'color':
                '#720096'}, {'id': 35551, 'name': 'query_module_signature_generator.py', 'path':
                'memgraph-gqlalchemy-7fbec93/scripts/query_module_signature_generator.py', 'size': 16.90260223043564, 'color':
                '#720096'}, {'id': 35562, 'name': 'test_query_modules.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/graph_algorithms/test_query_modules.py', 'size': 16.90260223043564, 'color':
                '#720096'}, {'id': 35565, 'name': 'test_graph_algorithms.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/integration/test_graph_algorithms.py', 'size': 16.90260223043564, 'color':
                '#720096'}, {'id': 35557, 'name': 'test_query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/docs/test_query_builder.py', 'size': 16.90260223043564, 'color': '#FFC500'}, {'id':
                35556, 'name': 'test_ogm.py', 'path': 'memgraph-gqlalchemy-7fbec93/tests/docs/test_ogm.py', 'size': 16.90260223043564,
            'color': '#FFC500'}, {'id': 35575, 'name': 'test_memgraph.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/memgraph/test_memgraph.py', 'size': 16.90260223043564, 'color': '#720096'}], 'links':
        [{'source': 35488, 'target': 35532}, {'source': 35488, 'target': 35490}, {'source': 35488, 'target': 35530}, {'source':
                35488, 'target': 35491}, {'source': 35488, 'target': 35534}, {'source': 35488, 'target': 35535}, {'source': 35488,
            'target': 35536}, {'source': 35488, 'target': 35545}, {'source': 35488, 'target': 35546}, {'source': 35544, 'target':
                35489}, {'source': 35545, 'target': 35489}, {'source': 35546, 'target': 35489}, {'source': 35489, 'target': 35546},
            {'source': 35489, 'target': 35491}, {'source': 35489, 'target': 35532}, {'source': 35488, 'target': 35490}, {'source':
                35545, 'target': 35490}, {'source': 35488, 'target': 35491}, {'source': 35489, 'target': 35491}, {'source': 35530,
            'target': 35491}, {'source': 35532, 'target': 35491}, {'source': 35534, 'target': 35491}, {'source': 35544, 'target':
                35491}, {'source': 35545, 'target': 35491}, {'source': 35546, 'target': 35491}, {'source': 35566, 'target': 35491},
            {'source': 35569, 'target': 35491}, {'source': 35574, 'target': 35491}, {'source': 35592, 'target': 35491}, {'source':
                35593, 'target': 35491}, {'source': 35488, 'target': 35530}, {'source': 35553, 'target': 35530}, {'source': 35593,
            'target': 35530}, {'source': 35530, 'target': 35491}, {'source': 35530, 'target': 35545}, {'source': 35474, 'target':
                35531}, {'source': 35531, 'target': 35532}, {'source': 35531, 'target': 35535}, {'source': 35488, 'target': 35532},
            {'source': 35489, 'target': 35532}, {'source': 35531, 'target': 35532}, {'source': 35534, 'target': 35532}, {'source':
                35541, 'target': 35532}, {'source': 35544, 'target': 35532}, {'source': 35545, 'target': 35532}, {'source': 35546,
            'target': 35532}, {'source': 35566, 'target': 35532}, {'source': 35568, 'target': 35532}, {'source': 35570, 'target':
                35532}, {'source': 35577, 'target': 35532}, {'source': 35532, 'target': 35491}, {'source': 35568, 'target': 35541},
            {'source': 35598, 'target': 35541}, {'source': 35541, 'target': 35532}, {'source': 35541, 'target': 35542}, {'source':
                35534, 'target': 35542}, {'source': 35541, 'target': 35542}, {'source': 35568, 'target': 35542}, {'source': 35590,
            'target': 35542}, {'source': 35591, 'target': 35542}, {'source': 35592, 'target': 35542}, {'source': 35598, 'target':
                35542}, {'source': 35599, 'target': 35542}, {'source': 35534, 'target': 35398}, {'source': 35590, 'target': 35398},
            {'source': 35559, 'target': 35529}, {'source': 35529, 'target': 35534}, {'source': 35529, 'target': 35535}, {'source':
                35529, 'target': 35545}, {'source': 35545, 'target': 35399}, {'source': 35551, 'target': 35399}, {'source': 35562,
            'target': 35399}, {'source': 35565, 'target': 35399}, {'source': 35488, 'target': 35534}, {'source': 35529, 'target':
                35534}, {'source': 35535, 'target': 35534}, {'source': 35536, 'target': 35534}, {'source': 35557, 'target': 35534},
            {'source': 35592, 'target': 35534}, {'source': 35534, 'target': 35491}, {'source': 35534, 'target': 35398}, {'source':
                35534, 'target': 35545}, {'source': 35534, 'target': 35532}, {'source': 35534, 'target': 35542}, {'source': 35534,
            'target': 35544}, {'source': 35488, 'target': 35535}, {'source': 35529, 'target': 35535}, {'source': 35531, 'target':
                35535}, {'source': 35556, 'target': 35535}, {'source': 35559, 'target': 35535}, {'source': 35590, 'target': 35535},
            {'source': 35535, 'target': 35534}, {'source': 35535, 'target': 35544}, {'source': 35535, 'target': 35545}, {'source':
                35488, 'target': 35536}, {'source': 35591, 'target': 35536}, {'source': 35536, 'target': 35534}, {'source': 35536,
            'target': 35546}, {'source': 35534, 'target': 35544}, {'source': 35535, 'target': 35544}, {'source': 35545, 'target':
                35544}, {'source': 35546, 'target': 35544}, {'source': 35544, 'target': 35489}, {'source': 35544, 'target': 35491},
            {'source': 35544, 'target': 35532}, {'source': 35488, 'target': 35545}, {'source': 35529, 'target': 35545}, {'source':
                35530, 'target': 35545}, {'source': 35534, 'target': 35545}, {'source': 35535, 'target': 35545}, {'source': 35557,
            'target': 35545}, {'source': 35575, 'target': 35545}, {'source': 35545, 'target': 35489}, {'source': 35545, 'target':
                35490}, {'source': 35545, 'target': 35491}, {'source': 35545, 'target': 35532}, {'source': 35545, 'target': 35544},
            {'source': 35545, 'target': 35399}, {'source': 35488, 'target': 35546}, {'source': 35489, 'target': 35546}, {'source':
                35536, 'target': 35546}, {'source': 35546, 'target': 35489}, {'source': 35546, 'target': 35491}, {'source': 35546,
            'target': 35532}, {'source': 35546, 'target': 35544}, {'source': 35551, 'target': 35399}, {'source': 35553, 'target':
                35530}, {'source': 35593, 'target': 35491}, {'source': 35593, 'target': 35530}, {'source': 35598, 'target': 35541},
            {'source': 35598, 'target': 35542}, {'source': 35599, 'target': 35542}, {'source': 35556, 'target': 35535}, {'source':
                35557, 'target': 35545}, {'source': 35557, 'target': 35534}, {'source': 35559, 'target': 35529}, {'source': 35559,
            'target': 35535}, {'source': 35562, 'target': 35399}, {'source': 35565, 'target': 35399}, {'source': 35566, 'target':
                35532}, {'source': 35566, 'target': 35491}, {'source': 35568, 'target': 35532}, {'source': 35568, 'target': 35541},
            {'source': 35568, 'target': 35542}, {'source': 35569, 'target': 35491}, {'source': 35570, 'target': 35532}, {'source':
                35474, 'target': 35531}, {'source': 35574, 'target': 35491}, {'source': 35575, 'target': 35545}, {'source': 35577,
            'target': 35532}, {'source': 35590, 'target': 35535}, {'source': 35590, 'target': 35398}, {'source': 35590, 'target':
                35542}, {'source': 35591, 'target': 35536}, {'source': 35591, 'target': 35542}, {'source': 35592, 'target': 35491},
            {'source': 35592, 'target': 35534}, {'source': 35592, 'target': 35542}], 'nodes_dict': {35532: {'id': 35532, 'name':
                'models.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/models.py', 'size': 32.300657744226726, 'color':
                '#FB6E00'}, 35488: {'id': 35488, 'name': '__init__.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/__init__.py',
            'size': 11.90260223043564, 'color': '#FFC500'}, 35490: {'id': 35490, 'name': 'disk_storage.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/disk_storage.py', 'size': 18.11416059218413, 'color': '#FFC500'}, 35530: {'id':
                35530, 'name': 'instance_runner.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/instance_runner.py', 'size':
                19.452820989308023, 'color': '#FFC500'}, 35491: {'id': 35491, 'name': 'exceptions.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/exceptions.py', 'size': 36.02661889114847, 'color': '#FB6E00'}, 35534: {'id':
                35534, 'name': 'declarative_base.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/query_builders/declarative_base.py', 'size': 19.627544147868136, 'color':
                '#FFC500'}, 35535: {'id': 35535, 'name': 'memgraph_query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/query_builders/memgraph_query_builder.py', 'size': 21.375955468813782, 'color':
                '#FFC500'}, 35536: {'id': 35536, 'name': 'neo4j_query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/query_builders/neo4j_query_builder.py', 'size': 17.431306119470158, 'color':
                '#FFC500'}, 35545: {'id': 35545, 'name': 'memgraph.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/vendors/memgraph.py', 'size': 25.23207008641456, 'color': '#FFC500'}, 35546:
            {'id': 35546, 'name': 'neo4j.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/vendors/neo4j.py', 'size':
                    21.106827473177553, 'color': '#FB6E00'}, 35544: {'id': 35544, 'name': 'database_client.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/vendors/database_client.py', 'size': 21.905794856008217, 'color': '#FB6E00'},
        35489: {'id': 35489, 'name': 'connection.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/connection.py', 'size':
                15.029286781758984, 'color': '#FB6E00'}, 35566: {'id': 35566, 'name': 'test_index.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/integration/test_index.py', 'size': 16.90260223043564, 'color': '#FB6E00'}, 35569:
            {'id': 35569, 'name': 'test_stream.py', 'path': 'memgraph-gqlalchemy-7fbec93/tests/integration/test_stream.py', 'size':
                    16.90260223043564, 'color': '#FB6E00'}, 35574: {'id': 35574, 'name': 'test_add_query_modules.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/memgraph/test_add_query_modules.py', 'size': 16.90260223043564, 'color': '#FB6E00'},
        35592: {'id': 35592, 'name': 'test_query_builders.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/query_builders/test_query_builders.py', 'size': 16.90260223043564, 'color':
                '#FB6E00'}, 35593: {'id': 35593, 'name': 'test_instance_runner.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/test_instance_runner.py', 'size': 16.90260223043564, 'color': '#FFC500'}, 35553:
            {'id': 35553, 'name': 'conftest.py', 'path': 'memgraph-gqlalchemy-7fbec93/tests/conftest.py', 'size': 16.90260223043564,
                'color': '#FFC500'}, 35474: {'id': 35474, 'name': 'test_loaders.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/loaders/test_loaders.py', 'size': 16.90260223043564, 'color': '#868089'}, 35531:
            {'id': 35531, 'name': 'loaders.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/loaders.py', 'size':
                    12.172137546414021, 'color': '#868089'}, 35541: {'id': 35541, 'name': 'transformations.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/transformations.py', 'size': 18.25027881032755, 'color': '#F9AF73'}, 35568:
            {'id': 35568, 'name': 'test_networkx.py', 'path': 'memgraph-gqlalchemy-7fbec93/tests/integration/test_networkx.py',
                'size': 16.90260223043564, 'color': '#F9AF73'}, 35570: {'id': 35570, 'name': 'test_trigger.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/integration/test_trigger.py', 'size': 16.90260223043564, 'color': '#FB6E00'}, 35577:
            {'id': 35577, 'name': 'test_automatic_deserialisation.py', 'path':
                    'memgraph-gqlalchemy-7fbec93/tests/ogm/test_automatic_deserialisation.py', 'size': 16.90260223043564, 'color':
                    '#FB6E00'}, 35598: {'id': 35598, 'name': 'test_transformations.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/test_transformations.py', 'size': 16.90260223043564, 'color': '#F9AF73'}, 35542:
            {'id': 35542, 'name': 'utilities.py', 'path': 'memgraph-gqlalchemy-7fbec93/gqlalchemy/utilities.py', 'size':
                    24.42847438533373, 'color': '#F9AF73'}, 35590: {'id': 35590, 'name': 'test_memgraph_query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/query_builders/test_memgraph_query_builder.py', 'size': 16.90260223043564, 'color':
                '#F9AF73'}, 35591: {'id': 35591, 'name': 'test_neo4j_query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/query_builders/test_neo4j_query_builder.py', 'size': 16.90260223043564, 'color':
                '#F9AF73'}, 35599: {'id': 35599, 'name': 'test_utilities.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/test_utilities.py', 'size': 16.90260223043564, 'color': '#F9AF73'}, 35398: {'id':
                35398, 'name': 'integrated_algorithms.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/graph_algorithms/integrated_algorithms.py', 'size': 38.89566258187239, 'color':
                '#DC2223'}, 35559: {'id': 35559, 'name': 'test_query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/graph_algorithms/test_query_builder.py', 'size': 16.90260223043564, 'color':
                '#FFC500'}, 35529: {'id': 35529, 'name': 'query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/graph_algorithms/query_builder.py', 'size': 12.711208178370786, 'color':
                '#FFC500'}, 35399: {'id': 35399, 'name': 'query_modules.py', 'path':
                'memgraph-gqlalchemy-7fbec93/gqlalchemy/graph_algorithms/query_modules.py', 'size': 36.54714629362779, 'color':
                '#720096'}, 35551: {'id': 35551, 'name': 'query_module_signature_generator.py', 'path':
                'memgraph-gqlalchemy-7fbec93/scripts/query_module_signature_generator.py', 'size': 16.90260223043564, 'color':
                '#720096'}, 35562: {'id': 35562, 'name': 'test_query_modules.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/graph_algorithms/test_query_modules.py', 'size': 16.90260223043564, 'color':
                '#720096'}, 35565: {'id': 35565, 'name': 'test_graph_algorithms.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/integration/test_graph_algorithms.py', 'size': 16.90260223043564, 'color':
                '#720096'}, 35557: {'id': 35557, 'name': 'test_query_builder.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/docs/test_query_builder.py', 'size': 16.90260223043564, 'color': '#FFC500'}, 35556:
            {'id': 35556, 'name': 'test_ogm.py', 'path': 'memgraph-gqlalchemy-7fbec93/tests/docs/test_ogm.py', 'size':
                    16.90260223043564, 'color': '#FFC500'}, 35575: {'id': 35575, 'name': 'test_memgraph.py', 'path':
                'memgraph-gqlalchemy-7fbec93/tests/memgraph/test_memgraph.py', 'size': 16.90260223043564, 'color': '#720096'}}}


const Index: NextPage = () => {
    return (
        <>

            <Grid container justifyContent={"space-between"} alignItems={"stretch"} sx={{width: "100%", backgroundColor: "#F9F9F9", minHeight: "68vh", pb: "10px"}}>
                <Grid item lg={5} md={5} sm={12} xs={12} sx={{minHeight: "100%"}}>
                    <Box sx={{display: "flex", justifyContent: "end", alignItems: "center", height: "100%"}}>
                        <Stack direction={"column"} justifyContent={"center"} alignContent={"center"} spacing={4} sx={{height: "100%", paddingLeft: "4rem", paddingRight: "2rem", paddingTop: "2rem", paddingBottom: "2rem"}}>
                            <Typography variant={"h2"} sx={{fontWeight: "bold", color: "#211D1F"}}>GitHub Code Analyser</Typography>
                            <Typography  variant={"body2"}>Looking to improve your code? GitHub Code Analyser is an open source project that analyses your GitHub repositories and shows how you can improve your code. So what are you waiting? </Typography>
                            <Box sx={{display: "flex", justifyContent: "start", alignItems: "center"}}><Link href={"/repos"}><Button size={"large"} variant={"contained"} color={"primary"} sx={{textColor: "white", width: "200px"}}>Get Started</Button></Link></Box>
                            <Typography variant={"body2"}>Check out GitHub Code Analyser on <Link color={"black"} href={"https://github.com/memgraph/github-code-analysis/"}>GitHub</Link> <GitHub fontSize={"small"} /></Typography>
                        </Stack>
                    </Box>
                </Grid>
                <Grid item lg={7} md={7} sm={12} xs={12} sx={{minHeight: "100%", display: {xs: "none", sm: "none", md: "block"}}}>
                    <Box sx={{height: "100%"}} className={"index_page_graph"}>
                        <NetworkGraph data={graph_data} />
                    </Box>
                </Grid>
            </Grid>

            <Grid container sx={{display: "flex", justifyContent: "center", alignItems: "center", backgroundColor: "#F9F9F9", pt: "30px", pb: "30px"}}>
                <Grid item lg={8} md={10} sm={10} xs={11}>
                    <img src={"/cover_images/memgraph_sample_query_upscaled.png"} alt={"Memgraph Logo"} style={{width: "100%"}}/>
                </Grid>
            </Grid>

            <Stack spacing={2} direction={"row"} justifyContent={"center"} alignItems={"center"} sx={{padding: "1.5rem", background: "linear-gradient(90deg, rgba(255,197,0,1) 0%, rgba(220,34,35,1) 40%, rgba(114,0,150,1) 100%);", color: "white"}}>
                <Typography textAlign={"center"} variant={"body2"}>Powered by </Typography>
                <img src={"/logos/memgraph-white-logo.svg"} height={"32rem"} />
            </Stack>

        </>
    );
}


export default Index;