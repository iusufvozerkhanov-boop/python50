import sqlite3

# Пути к базам данных
TASKS_DB = "tasks.db"
COMPLETED_DB = "completed.db"

def init_db():
    """Инициализация таблиц в обеих базах данных"""
    # База активных задач
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

    # База выполненных задач
    conn = sqlite3.connect(COMPLETED_DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS completed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Функции для активных задач
def show_tasks() -> list:
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def insert_task(name: str) -> None:
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_task_by_id(task_id: int):
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def delete_task(task_id: int) -> None:
    conn = sqlite3.connect(TASKS_DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Функции для выполненных задач
def add_completed(name: str) -> None:
    conn = sqlite3.connect(COMPLETED_DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO completed (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def show_completed() -> list:
    conn = sqlite3.connect(COMPLETED_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM completed")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_completed_task(task_id: int) -> None:
    """Новая функция для удаления из архива"""
    conn = sqlite3.connect(COMPLETED_DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM completed WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()