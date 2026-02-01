from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from data import (
    init_db, show_tasks, insert_task, delete_task,
    add_completed, show_completed, get_task_by_id,
    create_user, get_user
)

app = Flask(__name__)
app.secret_key = "secret-key"

# ---------- INIT ----------
init_db()

# ---------- AUTHORS ----------
AUTHORS = {
    1: {"name": "Юсуф Python Coder", "role": "Lead Developer", "bio": "Я люблю программировать."},
    2: {"name": "Аскар Python Coder", "role": "Designer", "bio": "Отвечает за визуальный стиль приложения."},
    3: {"name": "Владислав Python Coder", "role": "Tester", "bio": "Следит за тем, чтобы все функции работали правильно."}
}

# ---------- AUTH DECORATOR ----------
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


# ---------- AUTH ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Заполните все поля ❌")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        try:
            create_user(username, password_hash)
            flash("Регистрация прошла успешно ✅")
            return redirect(url_for("login"))
        except:
            flash("Пользователь уже существует ❌")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = get_user(username)

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect(url_for("index"))

        flash("Неверный логин или пароль ❌")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Вы вышли из аккаунта 👋")
    return redirect(url_for("login"))


# ---------- MAIN ----------
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]

    if request.method == "POST":
        task = request.form.get("task")
        if task:
            insert_task(task, user_id)
        return redirect(url_for("index"))

    tasks = show_tasks(user_id)
    return render_template("index.html", tasks=tasks)


@app.route("/complete/<int:task_id>")
@login_required
def complete(task_id):
    user_id = session["user_id"]
    task = get_task_by_id(task_id, user_id)

    if task:
        add_completed(task[0], user_id)
        delete_task(task_id, user_id)

    return redirect(url_for("index"))


@app.route("/completed")
@login_required
def completed_page():
    completed = show_completed(session["user_id"])
    return render_template("completed.html", completed=completed)


@app.route("/delete/<int:task_id>")
@login_required
def delete(task_id):
    delete_task(task_id, session["user_id"])
    return redirect(url_for("index"))


# ---------- AUTHORS ----------
@app.route("/authors")
@login_required
def authors_page():
    return render_template("authors.html", authors=AUTHORS)


@app.route("/author/<int:author_id>")
@login_required
def author_detail(author_id):
    author = AUTHORS.get(author_id)
    if author:
        return render_template("author_detail.html", author=author)
    return render_template("404error.html"), 404


# ---------- ERRORS ----------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404error.html"), 404


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
