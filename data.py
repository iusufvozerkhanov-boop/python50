import sqlite3

DB = "todo.db"


# ---------- INIT ----------
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS completed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()
    conn.close()


# ---------- USERS ----------
def create_user(username: str, password_hash: str):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    conn.commit()
    conn.close()


def get_user(username: str):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user


# ---------- TASKS ----------
def show_tasks(user_id: int) -> list:
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name FROM tasks WHERE user_id = ?",
        (user_id,)
    )
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def insert_task(name: str, user_id: int) -> None:
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (name, user_id) VALUES (?, ?)",
        (name, user_id)
    )
    conn.commit()
    conn.close()


def get_task_by_id(task_id: int, user_id: int):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, user_id)
    )
    task = cursor.fetchone()
    conn.close()
    return task


def delete_task(task_id: int, user_id: int) -> None:
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, user_id)
    )
    conn.commit()
    conn.close()


# ---------- COMPLETED ----------
def add_completed(name: str, user_id: int) -> None:
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO completed (name, user_id) VALUES (?, ?)",
        (name, user_id)
    )
    conn.commit()
    conn.close()


def show_completed(user_id: int) -> list:
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name FROM completed WHERE user_id = ?",
        (user_id,)
    )
    tasks = cursor.fetchall()
    conn.close()
    return tasks
