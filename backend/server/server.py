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
from datetime import datetime


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


@app.route("/trending_repos", methods=["GET"])
def get_trending_repos():
    git_api_utils = GitApiUtils()
    repos = git_api_utils.get_trending_repos()
    return Response(json.dumps(list(map(get_important_repo_data, repos))), mimetype="application/json")


@app.route("/user/register", methods=['POST'])
def register_user():
    if not(request.form.get('login') and request.form.get('user_id')):
        return Response(status=401)
    return Response(json.dumps({"login": True}), status=200)


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


def get_important_repo_data(repo_data: dict):
    date_time_obj = datetime.strptime(repo_data.get("updated_at"), '%Y-%m-%dT%H:%M:%SZ')
    git_api_utils = GitApiUtils(request.form['access_token'])
    languages = list(git_api_utils.get_repo_languages(repo_data.get("full_name")).keys())
    return {"name": repo_data.get("name", ""), 
            "full_name": repo_data.get("full_name", ""), 
            "public": repo_data.get("visibility", "public") == "public", 
            "updated_at": date_time_obj.strftime("%d %b, %Y"), 
            "languages": languages,
            "github_url": repo_data.get("html_url"),}


@app.route("/repos", methods=['POST'])
def get_all_user_repos():
    if not(request.form.get('access_token')):
        return Response(status=401)
    
    if get_rate_limit(request.form['access_token']) < 2:
        return Response(status=429)

    git_api_utils = GitApiUtils(request.form['access_token'])
    repos = git_api_utils.get_all_user_repos()
    important_repo_data = list(map(get_important_repo_data, repos))
    starred_repos = git_api_utils.get_all_starred_repos()
    important_starred_repo_data = list(map(get_important_repo_data, starred_repos))

    return Response(json.dumps({"repos": important_repo_data, "starred": important_starred_repo_data}), status=200)


if __name__ == '__main__':
    logging.info("Backend is ready.")
    app.run(debug = True, host="127.0.0.1", port="5000")
