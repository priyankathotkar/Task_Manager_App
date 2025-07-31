import sqlite3
import hashlib
from datetime import datetime

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self._enable_foreign_keys()
        self._ensure_schema()

    def _enable_foreign_keys(self):
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def _ensure_schema(self):
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                last_login TIMESTAMP
            )
        ''')

        # Tasks table base (if not exists)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task TEXT NOT NULL,
                status TEXT DEFAULT "Pending",
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        # Inspect existing columns in tasks
        self.cursor.execute("PRAGMA table_info(tasks)")
        existing = {row[1] for row in self.cursor.fetchall()}  # column names

        # Add missing columns if needed
        if "due_date" not in existing:
            self.cursor.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")
        if "priority" not in existing:
            self.cursor.execute("ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'")

        # Commit after possible alterations
        self.conn.commit()

    # User management
    def _hash(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        hashed = self._hash(password)
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # already exists

    def login_user(self, username, password):
        hashed = self._hash(password)
        self.cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (username, hashed)
        )
        row = self.cursor.fetchone()
        if row:
            user_id = row[0]
            now = datetime.now()
            self.cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (now, user_id))
            self.conn.commit()
            return user_id
        return None

    def count_registered_users(self):
        self.cursor.execute("SELECT COUNT(*) FROM users")
        return self.cursor.fetchone()[0]

    def count_logged_in_users_today(self):
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE last_login >= ?", (today_start,))
        return self.cursor.fetchone()[0]

    # Task management
    def add_task(self, user_id, task, due_date=None, priority="Medium"):
        self.cursor.execute(
            "INSERT INTO tasks (user_id, task, due_date, priority) VALUES (?, ?, ?, ?)",
            (user_id, task, due_date, priority)
        )
        self.conn.commit()

    def get_tasks(self, user_id):
        self.cursor.execute(
            "SELECT id, task, status, due_date, priority FROM tasks WHERE user_id = ?",
            (user_id,)
        )
        return self.cursor.fetchall()

    def update_task_status(self, task_id, new_status):
        self.cursor.execute(
            "UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id)
        )
        self.conn.commit()

    def update_task(self, task_id, new_task=None, new_due_date=None, new_priority=None):
        updates = []
        params = []
        if new_task is not None:
            updates.append("task = ?")
            params.append(new_task)
        if new_due_date is not None:
            updates.append("due_date = ?")
            params.append(new_due_date)
        if new_priority is not None:
            updates.append("priority = ?")
            params.append(new_priority)
        if not updates:
            return
        params.append(task_id)
        sql = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(sql, tuple(params))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
