import json
import logging
from datetime import datetime
from multiprocessing import Process
from os import getenv
from time import sleep
from typing import Dict, Optional, List

from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_cors import CORS
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from backend.GitBackendUtils.GitApiUtils import GitApiUtils
from backend.MemgraphUtils.MemgraphInstance import MemgraphInstance
from backend.server.ServerConstants import ServerConstants

memgraph = MemgraphInstance.get_instance()
MEMGRAPH_FOUND = False
while not MEMGRAPH_FOUND:
    try:
        from backend.MemgraphUtils.UserUtils import UserUtils
        from backend.MemgraphUtils.RepoUtils import RepoUtils
        from backend.MemgraphUtils.BranchUtils import BranchUtils
        from backend.MemgraphUtils.CommitUtils import CommitUtils
        from backend.MemgraphUtils.StatusUtils import StatusUtils
        from backend.MemgraphUtils.FileUtils import FileUtils
        from backend.MemgraphUtils.Models import HasFile, Dir

        MEMGRAPH_FOUND = True
    except:
        logging.warning("Memgraph not found. Trying again.")
        sleep(1)

logging.basicConfig(
    filename=ServerConstants.LOGGING_FILE_PATH.value,
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)
logging.getLogger("kafka").setLevel(logging.WARNING)

load_dotenv()
app = Flask(__name__)
CORS(app)

BROKER_FOUND = False
while not BROKER_FOUND:
    try:
        producer = KafkaProducer(
            bootstrap_servers=f"{ServerConstants.KAFKA_IP.value}:{ServerConstants.KAFKA_PORT.value}"
        )
        BROKER_FOUND = True
    except NoBrokersAvailable:
        logging.warning("No broker available.")
        sleep(1)


## Helper functions


def get_rate_limit(access_token: str):
    git_api_utils = GitApiUtils(access_token)
    return git_api_utils.check_rate_limit().get("rate").get("remaining")


def get_repo_data_from_api_results(repo_data: Dict, starred=False) -> Dict:
    git_api_utils = GitApiUtils(request.form["access_token"])
    languages = list(git_api_utils.get_repo_languages(repo_data.get("full_name")).keys())
    return {
        "name": repo_data.get("name", ""),
        "full_name": repo_data.get("full_name", ""),
        "public": repo_data.get("visibility", "public") == "public",
        "updated_at": datetime.strptime(repo_data.get("pushed_at"), "%Y-%m-%dT%H:%M:%SZ"),
        "languages": languages,
        "github_url": repo_data.get("html_url"),
        "is_starred": starred,
        "id": repo_data.get("id"),
        "default_branch": repo_data.get("default_branch"),
    }


def check_if_user_exists(username: str, access_token: str) -> bool:
    user_utils = UserUtils(memgraph)
    git_api_utils = GitApiUtils(access_token)
    user_details = git_api_utils.get_user_info()
    login = user_details.get("login")

    if username != login:
        return False

    return user_utils.user_exists(username=login)


def check_necessary_data(
    necessary_data: Dict[str, Optional[str]], check_user: bool = True, rate_limit: int = 10
) -> Optional[Response]:
    if not all(necessary_data.values()):
        return Response(
            json.dumps({"error": "Missing necessary data."}),
            status=400,
            mimetype="application/json",
        )

    try:
        if check_user:
            try:
                if not check_if_user_exists(
                    username=necessary_data.get("login"), access_token=necessary_data.get("access_token")
                ):
                    return Response(json.dumps({"message": "User does not exist"}), status=401, mimetype="application/json")
            except: # Broken pipe error: quick fix
                if not check_if_user_exists(
                    username=necessary_data.get("login"), access_token=necessary_data.get("access_token")
                ):
                    return Response(json.dumps({"message": "User does not exist"}), status=401, mimetype="application/json")

            if get_rate_limit(access_token=necessary_data.get("access_token")) < rate_limit:
                return Response(json.dumps({"message": "Rate limit exceeded"}), status=429, mimetype="application/json")
    except:
        return Response(json.dumps({"message": "Something went wrong"}), status=500, mimetype="application/json")


def fill_memgraph_with_repo_data(username: str, access_token: str) -> None:
    git_api_utils = GitApiUtils(access_token)
    repos = git_api_utils.get_all_user_repos(first_page_only=False, start_page=1)
    starred_repos = git_api_utils.get_all_starred_repos(first_page_only=False, start_page=1)

    repo_utils = RepoUtils(memgraph)

    starred_repos_full_name = list(map(lambda repo_data: repo_data.get("id"), starred_repos))

    repos_to_save = []

    for repo in repos:
        if repo.get("id") not in starred_repos_full_name:
            repos_to_save.append(get_repo_data_from_api_results(repo))

    for starred_repo in starred_repos:
        repos_to_save.append(get_repo_data_from_api_results(starred_repo, starred=True))

    if len(repos_to_save) > 0:
        repo_utils.save_repositories(username=username, repo_list=repos_to_save)


def get_all_user_repositories(username: str) -> str:
    repo_utils = RepoUtils(memgraph)
    important_repo_data = list(
        map(
            repo_utils.map_repo_object_to_json,
            map(lambda repo: repo.get("repository"), repo_utils.get_repositories(username=username)),
        )
    )
    important_starred_repo_data = list(
        map(
            lambda repo: repo_utils.map_repo_object_to_json(repo, True),
            map(
                lambda repo: repo.get("repository"),
                repo_utils.get_repositories(username=username, all=False, is_starred=True),
            ),
        )
    )

    return json.dumps({"repos": important_repo_data, "starred": important_starred_repo_data})


def create_filetree_graph(filetree: List[Dict]) -> Dict:
    if len(filetree) == 0:
        return {}

    hierarchy_dict = {"name": filetree[0].get("name"), "children": []}
    files_dict = {}
    for record in filetree[1:]:
        files_dict[record.get("path")] = record
        folder = hierarchy_dict
        for subfolder in record.get("path").split("/")[:-1]:
            for child in folder.get("children"):
                if child.get("name") == subfolder:
                    folder = child
                    break

        if record.get("label") == "File":
            folder["children"].append({"name": record.get("name"), "attributes": {"type": "file"}})
        else:
            folder["children"].append({"name": record.get("name"), "attributes": {"type": "dir"}, "children": []})

    return hierarchy_dict


def start_filetree_creation(username: str, repo_name: str, access_token: str, commit_sha: str) -> None:
    producer.send(
        topic=ServerConstants.KAFKA_TO_CORE_TOPIC.value,
        value=ServerConstants.KAFKA_DOWNLOAD_AND_GET_ALL_FORMAT.value.format(
            username=username,
            repo_name=repo_name,
            commit_sha=commit_sha,
            access_token=access_token,
        ).encode("utf-8"),
    )


## Routes


@app.route("/trending-repos", methods=["POST"])
def get_trending_repos():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "login": request.form.get("login"),
        }
    )

    if check:
        return check

    git_api_utils = GitApiUtils()
    repos = git_api_utils.get_trending_repos()
    return Response(json.dumps(repos), status=200)


@app.route("/user/register", methods=["POST"])
def register_user():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "secret_key": request.form.get("secret_key"),
            "login": request.form.get("login"),
        },
        check_user=False,
    )

    if check:
        return check

    if getenv("SECRET_REGISTRATION_KEY") != request.form.get("secret_key"):
        return Response(status=401)

    user_utils = UserUtils(memgraph)

    if not user_utils.user_exists(username=request.form.get("login")):
        user_utils.save_user(username=request.form.get("login"))
        p = Process(
            target=fill_memgraph_with_repo_data, args=(request.form.get("login"), request.form.get("access_token"))
        )
        p.start()

    return Response(json.dumps({"login": True}), status=200)


@app.route("/repos", methods=["POST"])
def get_all_user_repos():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "login": request.form.get("login"),
        },
        check_user=True,
    )

    if check:
        return check

    return Response(get_all_user_repositories(username=request.form.get("login")), status=200)


@app.route("/refresh-repos", methods=["POST"])
def refresh_repos():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "login": request.form.get("login"),
        },
        check_user=True,
    )

    if check:
        return check

    repo_utils = RepoUtils(memgraph)
    memgraph_user_repos_results = repo_utils.get_repositories(username=request.form.get("login"))

    id_repo_memgraph_dict = {}
    repo_id_edge_memgraph_dict = {}
    memgraph_repos_id = set()
    memgraph_starred_repos_id = set()

    for repo in memgraph_user_repos_results:
        id_repo_memgraph_dict[repo.get("repository").repo_id] = repo.get("repository")
        repo_id_edge_memgraph_dict[repo.get("repository").repo_id] = repo.get("edge")
        memgraph_repos_id.add(repo.get("repository").repo_id)
        if repo.get("edge").is_starred:
            memgraph_starred_repos_id.add(repo.get("repository").repo_id)

    git_api_utils = GitApiUtils(request.form.get("access_token"))
    git_repos = git_api_utils.get_all_user_repos(first_page_only=False)
    git_starred_repos = git_api_utils.get_all_starred_repos(first_page_only=False)

    id_repo_dict = dict(map(lambda git_repo: (git_repo.get("id"), git_repo), git_repos))
    id_repo_starred_dict = dict(map(lambda git_repo: (git_repo.get("id"), git_repo), git_starred_repos))

    starred_repos_id = set(id_repo_starred_dict.keys())
    repos_id = set(filter(lambda git_repo_id: git_repo_id not in starred_repos_id, id_repo_dict.keys()))

    repos_to_save = []
    repos_to_update = []
    repos_to_detach = []
    edges_to_update = []

    for repo_id in starred_repos_id:
        if repo_id not in memgraph_repos_id:
            repos_to_save.append(get_repo_data_from_api_results(id_repo_starred_dict[repo_id], starred=True))
        elif repo_utils.repo_needs_updating(id_repo_starred_dict[repo_id], id_repo_memgraph_dict[repo_id]):
            repos_to_update.append(get_repo_data_from_api_results(id_repo_starred_dict[repo_id], starred=True))

    for repo_id in repos_id:
        if repo_id not in memgraph_repos_id:
            repos_to_save.append(get_repo_data_from_api_results(id_repo_dict[repo_id]))
        elif repo_utils.repo_needs_updating(id_repo_dict[repo_id], id_repo_memgraph_dict[repo_id]):
            repos_to_update.append(get_repo_data_from_api_results(id_repo_dict[repo_id]))

    for repo_id in memgraph_repos_id:
        if repo_id not in repos_id and repo_id not in starred_repos_id:
            repos_to_detach.append(id_repo_memgraph_dict[repo_id])
        elif repo_id in repos_id and repo_id not in starred_repos_id and repo_id_edge_memgraph_dict[repo_id].is_starred:
            edges_to_update.append({"repo_id": repo_id, "is_starred": False})
        elif (
            repo_id in starred_repos_id
            and repo_id not in repos_id
            and not repo_id_edge_memgraph_dict[repo_id].is_starred
        ):
            edges_to_update.append({"repo_id": repo_id, "is_starred": True})

    # repo_utils.detach_repositories(username=request.form.get("login"), repo_list=repos_to_detach)
    repo_utils.update_edges(username=request.form.get("login"), repo_id_list=edges_to_update)
    repo_utils.save_repositories(username=request.form.get("login"), repo_list=repos_to_save)
    repo_utils.update_repositories(repo_list=repos_to_update)

    return Response(get_all_user_repositories(username=request.form.get("login")), status=200)


@app.route("/search-repos", methods=["POST"])
def search_repos():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "login": request.form.get("login"),
            "query": request.form.get("query"),
        },
        check_user=True,
    )

    if check:
        return check

    if request.form.get("query") == "":
        return Response(json.dumps([]), status=200)

    git_api_utils = GitApiUtils(request.form.get("access_token"))

    search_results = list(
        map(
            lambda repo: {
                "full_name": repo.get("full_name"),
                "description": repo.get("description"),
                "github_url": repo.get("html_url"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count"),
            },
            git_api_utils.search_for_repos(request.form.get("query")),
        )
    )

    return Response(json.dumps(search_results), status=200)


@app.route("/verify-repo", methods=["POST"])
def verify_repo():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "login": request.form.get("login"),
            "full_name": request.form.get("full_name"),
        },
        check_user=True,
    )

    if check:
        return check

    git_api_utils = GitApiUtils(request.form.get("access_token"))
    if git_api_utils.repo_exists(request.form.get("full_name")):
        return Response(status=200)

    return Response(status=404)


@app.route("/get-branches", methods=["POST"])
def get_branches():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "login": request.form.get("login"),
            "full_name": request.form.get("full_name"),
        },
        check_user=True,
    )

    if check:
        return check

    git_api_utils = GitApiUtils(request.form.get("access_token"))
    if not git_api_utils.repo_exists(request.form.get("full_name")):
        return Response(status=404)

    repo_utils = RepoUtils(memgraph)
    if not repo_utils.repo_exists(full_name=request.form.get("full_name")):
        repo_utils.save_repositories(
            username=request.form.get("login"),
            repo_list=[
                get_repo_data_from_api_results(
                    repo_data=git_api_utils.get_single_repo_info(request.form.get("full_name"))
                )
            ],
        )

    if not repo_utils.is_repo_connected(full_name=request.form.get("full_name"), username=request.form.get("login")):
        repo_utils.connect_repo(full_name=request.form.get("full_name"), username=request.form.get("login"))

    branch_utils = BranchUtils(memgraph)
    branches = branch_utils.get_branches_for_repo(user_repo=request.form.get("full_name"))

    formatted_branches = list(
        map(
            lambda branch: branch_utils.map_branch_object_to_json(branch.get("branch")),
            branches,
        )
    )

    if len(formatted_branches) == 0:
        git_branches = git_api_utils.get_all_repo_branches(request.form.get("full_name"), first_page_only=False)
        branch_utils.save_branches(user_repo=request.form.get("full_name"), branch_list=git_branches)
        branches = branch_utils.get_branches_for_repo(user_repo=request.form.get("full_name"))
        formatted_branches = list(
            map(
                lambda branch: branch_utils.map_branch_object_to_json(branch.get("branch")),
                branches,
            )
        )

    default_branch = repo_utils.get_default_branch(full_name=request.form.get("full_name"))

    return Response(json.dumps({"branches": formatted_branches, "default_branch": default_branch}), status=200)


@app.route("/refresh-branches", methods=["POST"])
def refresh_branches():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "login": request.form.get("login"),
            "full_name": request.form.get("full_name"),
        },
        check_user=True,
    )

    if check:
        return check

    git_api_utils = GitApiUtils(request.form.get("access_token"))
    if not git_api_utils.repo_exists(request.form.get("full_name")):
        return Response(status=404)

    git_branches = git_api_utils.get_all_repo_branches(user_repo=request.form.get("full_name"), first_page_only=False)
    git_branches_names_set = set(map(lambda branch: branch.get("name"), git_branches))
    name_branch_dict = {branch.get("name"): branch for branch in git_branches}
    branch_utils = BranchUtils(memgraph)
    repo_utils = RepoUtils(memgraph)
    branches = list(
        map(
            lambda branch: branch.get("branch"),
            branch_utils.get_branches_for_repo(user_repo=request.form.get("full_name")),
        )
    )
    memgraph_branches_names_set = set(map(lambda branch: branch.name, branches))
    memgraph_name_branch_dict = {branch.name: branch for branch in branches}
    branches_to_delete = memgraph_branches_names_set - git_branches_names_set
    branches_to_add = git_branches_names_set - memgraph_branches_names_set
    branches_to_update = set(
        filter(
            lambda lambda_branch_name: branch_utils.branch_needs_updating(
                git_branch_data=name_branch_dict[lambda_branch_name],
                memgraph_branch_data=memgraph_name_branch_dict[lambda_branch_name],
            ),
            memgraph_branches_names_set & git_branches_names_set,
        )
    )

    branch_utils.save_branches(
        user_repo=request.form.get("full_name"), branch_list=[name_branch_dict[branch] for branch in branches_to_add]
    )
    branch_utils.delete_branches(user_repo=request.form.get("full_name"), branch_list=list(branches_to_delete))
    for branch_name in branches_to_update:
        branch_utils.update_branch(
            user_repo=request.form.get("full_name"),
            branch_data=name_branch_dict[branch_name],
        )

    formatted_branches = list(
        map(
            lambda branch: branch_utils.map_branch_object_to_json(branch.get("branch")),
            branch_utils.get_branches_for_repo(user_repo=request.form.get("full_name")),
        )
    )

    default_branch = repo_utils.get_default_branch(full_name=request.form.get("full_name"))

    return Response(json.dumps({"branches": formatted_branches, "default_branch": default_branch}), status=200)


@app.route("/get-commits", methods=["POST"])
def get_commits():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "login": request.form.get("login"),
            "full_name": request.form.get("full_name"),
            "branch": request.form.get("branch"),
        },
        check_user=True,
    )

    if check:
        return check

    git_api_utils = GitApiUtils(request.form.get("access_token"))
    if not git_api_utils.repo_exists(request.form.get("full_name")):
        return Response(status=404)

    branch_utils = BranchUtils(memgraph)
    branch = branch_utils.get_branch(user_repo=request.form.get("full_name"), branch_name=request.form.get("branch"))
    if not branch:
        return Response(status=404)

    commit_utils = CommitUtils(memgraph)
    commits = commit_utils.get_commits_for_branch(
        user_repo=request.form.get("full_name"), branch_name=request.form.get("branch")
    )

    formatted_commits = list(
        map(
            lambda commit: commit_utils.map_commit_object_to_json(commit.get("commit")),
            commits,
        )
    )

    if len(formatted_commits) == 0:
        git_commits = git_api_utils.get_all_commits_for_branch(
            user_repo=request.form.get("full_name"), branch_sha=branch.commit_id
        )
        commit_utils.save_commits(
            user_repo=request.form.get("full_name"),
            branch_name=request.form.get("branch"),
            commit_list=git_commits,
        )
        commits = commit_utils.get_commits_for_branch(
            user_repo=request.form.get("full_name"), branch_name=request.form.get("branch")
        )
        formatted_commits = list(
            map(
                lambda commit: commit_utils.map_commit_object_to_json(commit.get("commit")),
                commits,
            )
        )

    return Response(json.dumps(formatted_commits), status=200)


@app.route("/refresh-commits", methods=["POST"])
def refresh_commits():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "login": request.form.get("login"),
            "full_name": request.form.get("full_name"),
            "branch": request.form.get("branch"),
        },
        check_user=True,
    )

    if check:
        return check

    git_api_utils = GitApiUtils(request.form.get("access_token"))
    if not git_api_utils.repo_exists(request.form.get("full_name")):
        return Response(status=404)

    branch_utils = BranchUtils(memgraph)
    branch = branch_utils.get_branch(user_repo=request.form.get("full_name"), branch_name=request.form.get("branch"))
    if not branch:
        return Response(status=404)

    git_commits = git_api_utils.get_all_commits_for_branch(
        user_repo=request.form.get("full_name"), branch_sha=branch.commit_id
    )
    git_commits_hashes = set(map(lambda commit: commit.get("sha"), git_commits))
    git_hash_commit_dict = {commit.get("sha"): commit for commit in git_commits}

    commit_utils = CommitUtils(memgraph)
    commits = commit_utils.get_commits_for_branch(
        user_repo=request.form.get("full_name"), branch_name=request.form.get("branch")
    )
    formatted_commits = list(map(lambda commit: commit.get("commit"), commits))
    memgraph_commits_hashes = set(map(lambda commit: commit.commit_id, formatted_commits))

    new_commits = git_commits_hashes - memgraph_commits_hashes
    new_commits_list = list(map(lambda commit_hash: git_hash_commit_dict[commit_hash], new_commits))
    commit_utils.save_commits(
        user_repo=request.form.get("full_name"),
        branch_name=request.form.get("branch"),
        commit_list=new_commits_list,
    )

    formatted_commits = list(
        map(
            lambda commit: commit_utils.map_commit_object_to_json(commit.get("commit")),
            commits,
        )
    )

    return Response(json.dumps(formatted_commits), status=200)


@app.route("/get-graphs", methods=["POST"])
def get_graphs():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "login": request.form.get("login"),
            "full_name": request.form.get("full_name"),
            "branch": request.form.get("branch"),
            "commit": request.form.get("commit"),
        },
        check_user=True,
    )

    if check:
        return check

    git_api_utils = GitApiUtils(request.form.get("access_token"))
    if not git_api_utils.repo_exists(request.form.get("full_name")):
        return Response(status=404)

    branch_utils = BranchUtils(memgraph)
    branch = branch_utils.get_branch(user_repo=request.form.get("full_name"), branch_name=request.form.get("branch"))
    if not branch:
        return Response(status=404)

    commit_utils = CommitUtils(memgraph)
    commit = commit_utils.get_commit(branch_name=request.form.get("branch"), commit_id=request.form.get("commit"))
    if not commit:
        return Response(status=404)

    status_utils = StatusUtils(memgraph)
    status = status_utils.get_commit_status(commit_id=commit.commit_id)

    if not status:
        return Response(json.dumps({"data": {}, "status": "new"}), status=200)

    file_utils = FileUtils(memgraph)
    files = file_utils.get_filetree_for_commit(commit_id=commit.commit_id)
    dependencies = file_utils.get_dependencies(commit_id=commit.commit_id)

    if not files:
        return Response(json.dumps({"data": {}, "status": status}), status=200)

    graphs = {}

    formatted_filetree = create_filetree_graph(files)

    graphs["File Tree"] = formatted_filetree
    graphs["Dependencies"] = dependencies

    return Response(json.dumps({"data": graphs, "status": status}), status=200)


@app.route("/start-graph-builder", methods=["POST"])
def start_graph_builder():
    check = check_necessary_data(
        necessary_data={
            "access_token": request.form.get("access_token"),
            "login": request.form.get("login"),
            "full_name": request.form.get("full_name"),
            "branch": request.form.get("branch"),
        },
        check_user=True,
    )

    if check:
        return check

    git_api_utils = GitApiUtils(request.form.get("access_token"))
    if not git_api_utils.repo_exists(request.form.get("full_name")):
        return Response(status=404)

    branch_utils = BranchUtils(memgraph)
    branch = branch_utils.get_branch(user_repo=request.form.get("full_name"), branch_name=request.form.get("branch"))
    if not branch:
        return Response(status=404)

    commit_utils = CommitUtils(memgraph)
    commits = commit_utils.get_commits_for_branch(
        user_repo=request.form.get("full_name"), branch_name=request.form.get("branch")
    )
    status_utils = StatusUtils(memgraph)

    for commit in commits:
        status = status_utils.get_commit_status(commit_id=commit.get("commit").commit_id)
        if not status:
            status_utils.add_status_to_commit(commit_id=commit.get("commit").commit_id, status="loading")
            username, repo = request.form.get("full_name").split("/")
            start_filetree_creation(
                username=username,
                repo_name=repo,
                commit_sha=commit.get("commit").commit_id,
                access_token=request.form.get("access_token"),
            )

    return Response(status=200)


if __name__ == "__main__":
    logging.info("Backend is ready.")
    app.run(debug=True, host="127.0.0.1", port=5000)
