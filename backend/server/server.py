from os import getenv
from flask import Flask, request, Response
from flask_cors import CORS
import json
from kafka import KafkaProducer
from backend.GitBackendUtils.GitApiUtils import GitApiUtils
from backend.server.ServerConstants import ServerConstants
from kafka.errors import NoBrokersAvailable
import logging
from time import sleep


logging.basicConfig(filename=ServerConstants.LOGGING_FILE_PATH.value,
                    level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger("kafka").setLevel(logging.WARNING)


app = Flask(__name__)
CORS(app)


broker_found = False
while not broker_found:
    try:
        producer = KafkaProducer(bootstrap_servers=f'{ServerConstants.KAFKA_IP.value}:{ServerConstants.KAFKA_PORT.value}')
        broker_found = True
    except NoBrokersAvailable:
        logging.warning("No broker available.")
        sleep(1)


def get_rate_limit(access_token: str):
    git_api_utils = GitApiUtils(access_token)
    return git_api_utils.check_rate_limit().get("rate").get("remaining")


@app.route("/", methods=['POST'])
def run_repo_parser():
    if not(request.form['user'] and request.form['repo'] and request.form['commit_hash'] and request.form['access_token']):
        return Response(status=400)

    if get_rate_limit(request.form['access_token']) == 0:
        return Response(status=429)
    
    producer.send(ServerConstants.KAFKA_TO_CORE_TOPIC.value, ServerConstants.KAFKA_DOWNLOAD_AND_GET_ALL_FORMAT.value.format(
            username=request.form.get("user"),
            repo_name=request.form.get("repo"),
            commit_sha=request.form.get("commit_hash"),
            access_token=request.form['access_token']
        ).encode("utf-8"))
    producer.close()

    return Response(json.dumps(ServerConstants.KAFKA_DOWNLOAD_AND_GET_ALL_FORMAT.value.format(
            username=request.form.get("user"),
            repo_name=request.form.get("repo"),
            commit_sha=request.form.get("commit_hash"),
            access_token=request.form['access_token']
        )), status=200)


if __name__ == '__main__':
    logging.info("Backend is ready.")
    app.run(debug = True, host="127.0.0.1", port="5000")
