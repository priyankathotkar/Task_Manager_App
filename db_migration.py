import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
    print("Column 'password' added to users table.")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")

conn.commit()
conn.close()
