# 🗂️ Task Manager Application

A **desktop task manager app** built with Python, designed to help users efficiently organize their tasks with due dates, user authentication, and password management — all wrapped in a clean and intuitive UI.  

---

## ✨ Features

- 🔐 **User Authentication:** Secure login and password reset functionality.  
- 📝 **Task Management:** Create, edit, delete, and mark tasks as complete.  
- 📅 **Due Date & Calendar:** Set deadlines and track upcoming tasks.  
- 👥 **User Inspection:** Administrative tools to monitor and manage users.  
- 🗄️ **Database Management:** Robust backend with schema migrations and CRUD operations.  
- 🎨 **Clean UI:** Modern interface enhanced with emojis for better user experience.  

---

### 🛠️ Technology Stack

- **Programming Language:** Python 🐍  
- **GUI Framework:** PyQt / PySide (Qt for Python) 🎨  
- **Database:** SQLite or other relational DB (via `db_manager.py`) 🗄️  

This combination allows building a responsive, user-friendly desktop app with robust backend support for task and user management.


## 📁 File Structure

| File Name           | Description                                  |
|---------------------|----------------------------------------------|
| `main.py`           | 🚀 Application entry point.                   |
| `db_manager.py`     | 🛠️ Database CRUD operations.                   |
| `db_migration.py`   | 🔧 Database schema setup and migrations.      |
| `login_ui.py`       | 🎭 Login dialog UI layout code.                |
| `login_dialog.py`   | 🔑 Login logic and user validation.            |
| `reset_password.py` | 🔄 Password reset UI and logic.                 |
| `inspect_user.py`   | 👁️ User inspection and admin features.          |

---

## ⚙️ Installation

1. Clone the repo:  
    ```bash
    git clone https://github.com/yourusername/task-manager-app.git
    cd task-manager-app
    ```

2. (Optional) Create & activate a virtual environment:  
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. Install dependencies (if available):  
    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database schema:  
    ```bash
    python db_migration.py
    ```

---

## ▶️ Usage

Run the app:  
```bash
python main.py

- 🔐 Log in or register a new user.

- 📝 Manage your tasks with due dates and completion status.

- 🔄 Reset your password anytime from the login screen.

- 👥 Admins can inspect user activities and manage permissions.

---

### 🤔 Why Use This App?

Organize your work and boost your productivity! This app offers:

- 🛡️ **Security:** Protect your tasks and data with authentication.

- 📅 **Organization:** Never miss deadlines with due date tracking.

- 🧩 **Scalability:** Supports multiple users and admin controls.

- 🔧 **Extensibility:** Modular design for easy customization and feature addition.

---

### 🤝 Contributing

Contributions are welcome! Feel free to:

- Fork the repository  
- Open issues  
- Submit pull requests  

