from os import getenv
from flask import Flask, request, Response
from flask_cors import CORS
import json
from kafka import KafkaProducer

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def hello_world():
    KAFKA_DOWNLOAD_AND_GET_ALL_FORMAT: str = '{{"query_type": "all_repository_information", "username": "{username}", "repo_name": "{repo_name}", "commit_sha": "{commit_sha}", "access_token": "{access_token}"}}'

    producer = KafkaProducer(bootstrap_servers='broker:9092')
    producer.send('to_core_data', KAFKA_DOWNLOAD_AND_GET_ALL_FORMAT.format(
            username=request.form.get("user"),
            repo_name=request.form.get("repo"),
            commit_sha=request.form.get("commit_hash"),
            access_token=getenv("ACCESS_TOKEN")
        ).encode("utf-8"))
    producer.close()

    return Response(json.dumps(KAFKA_DOWNLOAD_AND_GET_ALL_FORMAT.format(
            username=request.form.get("user"),
            repo_name=request.form.get("repo"),
            commit_sha=request.form.get("commit_hash"),
            access_token=getenv("ACCESS_TOKEN")
        )), status=200)


if __name__ == '__main__':
   app.run(debug = True, host="127.0.0.1", port="5000")
