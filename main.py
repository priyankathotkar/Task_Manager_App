import sys
from PyQt5.QtWidgets import QApplication
from db_manager import DBManager
from login_ui import LoginDialog
from ui_main import TaskManagerUI

def main():
    app = QApplication(sys.argv)
    db = DBManager()

    login_dialog = LoginDialog(db)
    if login_dialog.exec_() == LoginDialog.Accepted:
        user_id = login_dialog.user_id
        window = TaskManagerUI(user_id, db)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()

if __name__ == "__main__":
    main()
