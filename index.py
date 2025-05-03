from flask import Flask, render_template, request, jsonify
from ai_logic import score_task
import json
import os

app = Flask(__name__)

TASK_FILE = "tasks.json"

@app.route("/", methods=["GET"])
def index():
    with open(TASK_FILE, "r") as f:
        tasks = json.load(f)
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form["task"]
    with open(TASK_FILE, "r") as f:
        tasks = json.load(f)

    score = score_task(task_text)
    tasks.append({"task": task_text, "score": score})

    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f)

    return jsonify({"success": True, "score": score})

# Required for Vercel
def handler(environ, start_response):
    return app(environ, start_response)