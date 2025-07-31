from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

class LoginDialog(QDialog):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setWindowTitle("Login or Register")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

        self.user_id = None

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        user_id = self.db.verify_user(username, password)
        if user_id:
            self.user_id = user_id
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password.")

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        success = self.db.register_user(username, password)
        if success:
            QMessageBox.information(self, "Registration Successful", "You can now log in.")
        else:
            QMessageBox.warning(self, "Registration Failed", "Username already exists.")
