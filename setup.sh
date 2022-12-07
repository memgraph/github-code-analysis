#!/bin/bash

git clone --branch T291-MAGE_pagerank_subgraph https://github.com/memgraph/mage.git memgraph-mage
cd memgraph-mage
docker build -t memgraph-mage-custom .

cd ..
docker-compose build && docker-compose up