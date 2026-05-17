from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

# Load tasks from JSON file
def load_tasks():

    try:
        with open("tasks.json", "r") as file:
            return json.load(file)

    except:
        return []

# Save tasks into JSON file
def save_tasks(tasks):

    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

# Home page
@app.route("/")
def home():

    tasks = load_tasks()

    total = len(tasks)

    completed = sum(task["completed"] for task in tasks)

    pending = total - completed

    productivity = 0

    if total > 0:
        productivity = (completed / total) * 100

    return render_template(
        "index.html",
        tasks=tasks,
        total=total,
        completed=completed,
        pending=pending,
        productivity=productivity
    )

# Add task
@app.route("/add", methods=["POST"])
def add_task():

    tasks = load_tasks()

    new_task = {
        "title": request.form["title"],
        "priority": request.form["priority"],
        "due_date": request.form["due_date"],
        "completed": False
    }

    tasks.append(new_task)

    save_tasks(tasks)

    return redirect("/")

# Complete task
@app.route("/complete/<int:index>")
def complete_task(index):

    tasks = load_tasks()

    tasks[index]["completed"] = True

    save_tasks(tasks)

    return redirect("/")

# Delete task
@app.route("/delete/<int:index>")
def delete_task(index):

    tasks = load_tasks()

    tasks.pop(index)

    save_tasks(tasks)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)