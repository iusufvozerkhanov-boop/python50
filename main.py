from flask import Flask, render_template, request, redirect, url_for
from data import (
    show_tasks, insert_task, delete_task, init_db,
    add_completed, show_completed, get_task_by_id, delete_completed_task
)

app = Flask(__name__)
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    """Главная страница со списком задач"""
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            insert_task(task)
        return redirect(url_for("index"))
    tasks = show_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/complete/<int:task_id>")
def complete(task_id):
    """Перенос задачи в список выполненных"""
    task = get_task_by_id(task_id)
    if task:
        add_completed(task[0])
        delete_task(task_id)
    return redirect(url_for("index"))

@app.route("/completed")
def completed_page():
    """Страница архива выполненных задач"""
    completed = show_completed()
    return render_template("completed.html", completed=completed)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    """Удаление активной задачи"""
    delete_task(task_id)
    return redirect(url_for("index"))

@app.route("/delete_completed/<int:task_id>")
def delete_completed(task_id):
    """Удаление задачи из архива"""
    delete_completed_task(task_id)
    return redirect(url_for("completed_page"))

# Маршрут для второго сайта
@app.route("/other-site")
def other_site():
    return render_template("index1.html")

if __name__ == '__main__':
    app.run(debug=True)