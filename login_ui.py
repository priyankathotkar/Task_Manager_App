from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)

class LoginDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Login or Register")
        self.setFixedSize(320, 220)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
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
            QMessageBox.warning(self, "Input Error", "Please enter username and password.")
            return
        user_id = self.db.login_user(username, password)
        if user_id:
            self.user_id = user_id
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter username and password.")
            return
        success = self.db.register_user(username, password)
        if success:
            QMessageBox.information(self, "Registration Success", "User registered — you can now log in.")
        else:
            QMessageBox.warning(self, "Registration Failed", "Username already exists.")
