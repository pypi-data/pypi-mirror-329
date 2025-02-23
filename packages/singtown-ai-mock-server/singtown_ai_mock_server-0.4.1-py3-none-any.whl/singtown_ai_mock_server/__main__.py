from flask import Flask, abort, request, send_file
import os
import copy
from functools import wraps

TOKEN = "1234567890"

TASKS = [
    {
        "id": "b45f8ac0-a3a7-43ac-9d15-d2f4a505425c",
        "status": "pending",
        "crated_at": "2024-10-01T12:00:00Z",
        "cwd": "./singtown_ai",
        "dataset_path": "dataset",
        "metrics_path": "metrics.csv",
        "result_path": "result.zip",
        "cmd": [
            "python",
            "-u",
            "train.py",
        ],
    },
    {
        "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
        "status": "pending",
        "crated_at": "2023-10-01T12:00:00Z",
        "cwd": "./",
        "dataset_path": "dataset",
        "metrics_path": "metrics.csv",
        "result_path": "best.keras",
        "cmd": [
            "python",
            "-u",
            "train.py",
            "--model",
            "MobileNetV2",
            "--weight",
            "imagenet",
            "--alpha",
            "0.35",
            "--imgw",
            "224",
            "--imgh",
            "224",
            "--labels",
            "cat",
            "dog",
            "--epochs",
            "20",
            "--learning_rate",
            "0.001",
        ],
    },
    {
        "id": "321e8f2b-4c9d-4f5a-8b3e-2f7c8a1d6b4e",
        "status": "pending",
        "crated_at": "2023-10-01T12:00:00Z",
        "epochs": 5,
    },
]


def get_task_or_404(id: str):
    for t in copy.deepcopy(TASKS):
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


@app.post("/tasks/<id>")
@require_auth
def update_task(id: str):
    task = get_task_or_404(id)
    task.update(request.json)
    return "OK"


@app.post("/tasks/<id>/result")
@require_auth
def upload_task_result(id: str):
    get_task_or_404(id)
    result_path = os.path.join(app.static_folder, request.files["file"].filename)
    with open(result_path, "wb") as f:
        f.write(request.files["file"].read())
    return "OK"


@app.post("/tasks/<id>/log")
@require_auth
def upload_task_log(id: str):
    task = get_task_or_404(id)
    log = request.json["log"]
    task["log"] += log
    print(log)
    return "OK"


@app.get("/tasks/<id>/dataset")
@require_auth
def download_task_dataset(id: str):
    task = get_task_or_404(id)
    dataset_path = os.path.join(
        os.path.dirname(__file__), "datasets", f"{task['id']}.zip"
    )
    return send_file(dataset_path, as_attachment=True, download_name="dataset.zip")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
