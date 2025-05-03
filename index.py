from flask import Flask, render_template, request, redirect
from ai_logic import prioritize_tasks
import json
import os
from datetime import datetime

app = Flask(__name__)
TASK_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASK_FILE, 'w') as f:
        json.dump(tasks, f)

@app.route("/", methods=["GET", "POST"])
def index():
    tasks = load_tasks()

    if request.method == "POST":
        if "reset" in request.form:
            tasks = []
            save_tasks(tasks)
            return redirect("/")
        
        elif "edit" in request.form:
            index = int(request.form.get("edit_index"))
            new_name = request.form.get("edit_task").strip()
            if new_name:
                tasks[index]["name"] = new_name
                tasks[index]["timestamp"] = datetime.now().isoformat()
                tasks = prioritize_tasks(tasks)
                save_tasks(tasks)
            return redirect("/")

        else:  # Add new tasks
            input_text = request.form.get("tasks")
            if input_text:
                task_lines = input_text.strip().split("\n")
                new_tasks = [{"name": line.strip(), "timestamp": datetime.now().isoformat()} 
                             for line in task_lines if line.strip()]
                new_tasks = prioritize_tasks(new_tasks)
                tasks.extend(new_tasks)
                save_tasks(tasks)
            return redirect("/")  # Prevent resubmission on refresh

    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)