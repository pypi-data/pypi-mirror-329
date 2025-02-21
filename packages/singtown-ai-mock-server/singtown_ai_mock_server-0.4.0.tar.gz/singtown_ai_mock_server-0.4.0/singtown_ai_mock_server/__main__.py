from flask import Flask, abort, request
import os
import json
from functools import wraps

TOKEN = "1234567890"

TASKS = [
    {
        "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
        "project": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "status": "pending",
        "crated_at": "2023-10-01T12:00:00Z",
        "model": "MobileNetV2",
        "alpha": 1.0,
        "weight": "imagenet",
        "epochs": 20,
        "imgw": 224,
        "imgh": 224,
        "learning_rate": 0.001,
        "metrics": [{"epoch": 0, "metric": ""}],
        "log": "",
        "result": "",
    },
    {
        "id": "321e8f2b-4c9d-4f5a-8b3e-2f7c8a1d6b4e",
        "project": "d94f5e8c-7b3a-4e8f-9a2c-1b3d5f7a9c4e",
        "status": "pending",
        "crated_at": "2023-10-01T12:00:00Z",
        "epochs": 5,
        "metrics": [{"epoch": 0, "metric": ""}],
        "log": "",
        "result": "",
    },
]


def get_task_or_404(id: str):
    for t in TASKS:
        if t["id"] == id:
            return t
    abort(404)


app = Flask(__name__, static_url_path="/media", static_folder="media")


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get("Authorization") != f"Bearer {TOKEN}":
            abort(401)
        return f(*args, **kwargs)

    return decorated_function


@app.get("/tasks/<id>")
@require_auth
def get_task(id: str):
    task = get_task_or_404(id)
    return task


@app.get("/tasks/<id>/project")
@require_auth
def get_project(id: str):
    task = get_task_or_404(id)
    project_path = os.path.join(
        os.path.dirname(__file__), "projects", f"{task['project']}.json"
    )
    print(project_path)
    if not os.path.exists(project_path):
        return "Not Found", 404
    with open(project_path) as f:
        return json.load(f)


@app.post("/tasks/<id>/status")
@require_auth
def update_task_status(id: str):
    status = request.json["status"]
    task = get_task_or_404(id)
    task["status"] = status
    print(status)
    return "OK", 200


@app.post("/tasks/<id>/upload")
@require_auth
def upload_task_result(id: str):
    task = get_task_or_404(id)
    result_path = os.path.join(app.static_folder, request.files["file"].filename)
    with open(result_path, "wb") as f:
        f.write(request.files["file"].read())
    return "OK", 200


@app.post("/tasks/<id>/log")
@require_auth
def upload_task_log(id: str):
    task = get_task_or_404(id)
    log = request.json["log"]
    task["log"] += log
    print(log)
    return "OK", 200


@app.post("/tasks/<id>/metrics")
@require_auth
def upload_task_metrics(id: str):
    metric = request.json
    task = get_task_or_404(id)
    task["metrics"].append(metric)
    print(metric)
    return "OK", 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
