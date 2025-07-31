from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QLineEdit, QLabel,
    QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout,
    QMessageBox, QComboBox, QDateEdit, QHeaderView, QToolButton
)
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QColor, QBrush, QIcon
from datetime import datetime, timedelta

class TaskManagerUI(QMainWindow):
    def __init__(self, user_id, db):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 1000, 600)

        self.user_id = user_id
        self.db = db
        self.dark_mode = False

        # ===== toolbar-like controls =====
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tasks...")
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Pending", "Completed", "Overdue"])
        self.priority_filter = QComboBox()
        self.priority_filter.addItem("Any Priority")
        self.priority_filter.addItems(["High", "Medium", "Low"])
        self.due_from = QDateEdit()
        self.due_from.setCalendarPopup(True)
        self.due_from.setDisplayFormat("yyyy-MM-dd")
        self.due_from.setDate(QDate.currentDate().addDays(-7))
        self.due_to = QDateEdit()
        self.due_to.setCalendarPopup(True)
        self.due_to.setDisplayFormat("yyyy-MM-dd")
        self.due_to.setDate(QDate.currentDate().addDays(30))
        self.clear_filters_btn = QPushButton("Clear Filters")
        self.dark_toggle = QToolButton()
        self.dark_toggle.setText("Dark Mode")
        self.dark_toggle.setCheckable(True)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Search:"))
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(QLabel("Status:"))
        filter_layout.addWidget(self.status_filter)
        filter_layout.addWidget(QLabel("Priority:"))
        filter_layout.addWidget(self.priority_filter)
        filter_layout.addWidget(QLabel("Due From:"))
        filter_layout.addWidget(self.due_from)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(self.due_to)
        filter_layout.addWidget(self.clear_filters_btn)
        filter_layout.addWidget(self.dark_toggle)

        # ===== task entry row =====
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("New task description")
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDisplayFormat("yyyy-MM-dd")
        self.due_date_input.setDate(QDate.currentDate())
        self.priority_input = QComboBox()
        self.priority_input.addItems(["High", "Medium", "Low"])
        self.add_button = QPushButton("Add Task")
        self.add_button.setIcon(self.style().standardIcon(QPushButton().style().SP_DialogApplyButton))

        entry_layout = QHBoxLayout()
        entry_layout.addWidget(QLabel("Task:"))
        entry_layout.addWidget(self.task_input, 3)
        entry_layout.addWidget(QLabel("Due:"))
        entry_layout.addWidget(self.due_date_input)
        entry_layout.addWidget(QLabel("Priority:"))
        entry_layout.addWidget(self.priority_input)
        entry_layout.addWidget(self.add_button)

        # ===== table =====
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(["Task", "Status", "Due Date", "Priority", "Delete"])
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.task_table.setSortingEnabled(True)
        self.task_table.setSelectionBehavior(self.task_table.SelectRows)
        self.task_table.setEditTriggers(self.task_table.DoubleClicked | self.task_table.SelectedClicked)

        # ===== stats =====
        self.registered_label = QLabel()
        self.logged_in_today_label = QLabel()

        stats_layout = QHBoxLayout()
        stats_layout.addWidget(self.registered_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.logged_in_today_label)

        # ===== assemble =====
        main_layout = QVBoxLayout()
        main_layout.addLayout(filter_layout)
        main_layout.addLayout(entry_layout)
        main_layout.addWidget(self.task_table)
        main_layout.addLayout(stats_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # ===== signals =====
        self.add_button.clicked.connect(self.add_task)
        self.task_table.cellDoubleClicked.connect(self.toggle_status)
        self.task_table.cellChanged.connect(self.cell_edited)
        self.search_input.textChanged.connect(self.reload_tasks)
        self.status_filter.currentTextChanged.connect(self.reload_tasks)
        self.priority_filter.currentTextChanged.connect(self.reload_tasks)
        self.due_from.dateChanged.connect(self.reload_tasks)
        self.due_to.dateChanged.connect(self.reload_tasks)
        self.clear_filters_btn.clicked.connect(self.reset_filters)
        self.dark_toggle.toggled.connect(self.toggle_dark_mode)

        self.loading = False

        self.reload_tasks()
        self.update_user_stats()
        self.apply_light_theme()

    def reset_filters(self):
        self.search_input.clear()
        self.status_filter.setCurrentIndex(0)
        self.priority_filter.setCurrentIndex(0)
        self.due_from.setDate(QDate.currentDate().addDays(-7))
        self.due_to.setDate(QDate.currentDate().addDays(30))
        self.reload_tasks()

    def reload_tasks(self):
        self.loading = True
        self._update_overdue()
        tasks = self.db.get_tasks(self.user_id)

        keyword = self.search_input.text().strip().lower()
        status_filter = self.status_filter.currentText()
        priority_filter = self.priority_filter.currentText()
        due_from = self.due_from.date().toPyDate()
        due_to = self.due_to.date().toPyDate()

        self.task_table.setRowCount(0)
        for task_id, task, status, due_date, priority in tasks:
            if keyword and keyword not in task.lower():
                continue
            if status_filter != "All" and status != status_filter:
                continue
            if priority_filter != "Any Priority" and priority != priority_filter:
                continue
            if due_date:
                try:
                    due_dt = datetime.strptime(due_date, "%Y-%m-%d").date()
                except ValueError:
                    continue
                if due_dt < due_from or due_dt > due_to:
                    continue
            row = self.task_table.rowCount()
            self.task_table.insertRow(row)

            task_item = QTableWidgetItem(task)
            task_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self.task_table.setItem(row, 0, task_item)

            status_item = QTableWidgetItem(status)
            status_item.setFlags(status_item.flags() ^ Qt.ItemIsEditable)
            self.task_table.setItem(row, 1, status_item)

            due_item = QTableWidgetItem(due_date if due_date else "")
            due_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self.task_table.setItem(row, 2, due_item)

            prio_item = QTableWidgetItem(priority)
            prio_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            # color priority
            color = {"High": QColor(255, 200, 200), "Medium": QColor(255, 255, 200), "Low": QColor(200, 255, 200)}.get(priority, QColor(255, 255, 255))
            prio_item.setBackground(QBrush(color))
            self.task_table.setItem(row, 3, prio_item)

            delete_btn = QPushButton()
            delete_btn.setIcon(self.style().standardIcon(QPushButton().style().SP_TrashIcon if hasattr(QPushButton().style(), 'SP_TrashIcon') else QPushButton().style().SP_DialogCloseButton))
            delete_btn.setToolTip("Delete task")
            delete_btn.setFixedSize(QSize(32, 32))
            delete_btn.clicked.connect(lambda _, tid=task_id: self.delete_task(tid))
            self.task_table.setCellWidget(row, 4, delete_btn)

            # Row background for due soon / overdue
            if due_date:
                try:
                    due_dt = datetime.strptime(due_date, "%Y-%m-%d").date()
                    today = datetime.today().date()
                    if due_dt < today and status == "Pending":
                        # overdue
                        for c in range(5):
                            item = self.task_table.item(row, c)
                            if item:
                                item.setBackground(QBrush(QColor(255, 220, 220)))
                    elif 0 <= (due_dt - today).days <= 2:
                        for c in range(5):
                            item = self.task_table.item(row, c)
                            if item:
                                item.setBackground(QBrush(QColor(255, 245, 200)))
                except ValueError:
                    pass

        self.loading = False

    def _update_overdue(self):
        today = datetime.today().date()
        tasks = self.db.get_tasks(self.user_id)
        for task_id, task, status, due_date, priority in tasks:
            if due_date:
                try:
                    due = datetime.strptime(due_date, "%Y-%m-%d").date()
                    if due < today and status == "Pending":
                        self.db.update_task_status(task_id, "Overdue")
                except ValueError:
                    pass

    def add_task(self):
        task_text = self.task_input.text().strip()
        due_qdate = self.due_date_input.date().toPyDate()
        priority = self.priority_input.currentText()
        if not task_text:
            QMessageBox.warning(self, "Input Error", "Task cannot be empty.")
            return
        due_str = due_qdate.strftime("%Y-%m-%d")
        self.db.add_task(self.user_id, task_text, due_str, priority)
        self.task_input.clear()
        self.reload_tasks()

    def toggle_status(self, row, col):
        if col == 1:
            status_item = self.task_table.item(row, 1)
            if not status_item:
                return
            current = status_item.text()
            visible = self._visible_filtered_tasks()
            if row >= len(visible):
                return
            task_id = visible[row][0]
            new_status = "Completed" if current in ("Pending", "Overdue") else "Pending"
            self.db.update_task_status(task_id, new_status)
            self.reload_tasks()

    def cell_edited(self, row, column):
        if self.loading:
            return
        visible = self._visible_filtered_tasks()
        if row >= len(visible):
            return
        task_id = visible[row][0]
        new_value = self.task_table.item(row, column).text().strip()

        if column == 0:  # task text
            if new_value:
                self.db.update_task(task_id, new_task=new_value)
            else:
                self.reload_tasks()
        elif column == 2:  # due date
            if new_value:
                try:
                    datetime.strptime(new_value, "%Y-%m-%d")
                    self.db.update_task(task_id, new_due_date=new_value)
                except ValueError:
                    self.reload_tasks()
            else:
                self.db.update_task(task_id, new_due_date=None)
        elif column == 3:  # priority
            if new_value in ("High", "Medium", "Low"):
                self.db.update_task(task_id, new_priority=new_value)
            else:
                self.reload_tasks()

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        self.reload_tasks()

    def _visible_filtered_tasks(self):
        # reuse same filtering logic to get current list in order
        tasks = self.db.get_tasks(self.user_id)
        keyword = self.search_input.text().strip().lower()
        status_filter = self.status_filter.currentText()
        priority_filter = self.priority_filter.currentText()
        due_from = self.due_from.date().toPyDate()
        due_to = self.due_to.date().toPyDate()

        filtered = []
        for task in tasks:
            task_id, task_text, status, due_date, priority = task
            if keyword and keyword not in task_text.lower():
                continue
            if status_filter != "All" and status != status_filter:
                continue
            if priority_filter != "Any Priority" and priority != priority_filter:
                continue
            if due_date:
                try:
                    due_dt = datetime.strptime(due_date, "%Y-%m-%d").date()
                except ValueError:
                    continue
                if due_dt < due_from or due_dt > due_to:
                    continue
            filtered.append(task)
        return filtered

    def update_user_stats(self):
        registered = self.db.count_registered_users()
        logged_in_today = self.db.count_logged_in_users_today()
        self.registered_label.setText(f"Total Registered Users: {registered}")
        self.logged_in_today_label.setText(f"Users Logged in Today: {logged_in_today}")

    def toggle_dark_mode(self, on):
        self.dark_mode = on
        if on:
            self.apply_dark_theme()
            self.dark_toggle.setText("Light Mode")
        else:
            self.apply_light_theme()
            self.dark_toggle.setText("Dark Mode")

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background: #2b2b2b; color: #f0f0f0; }
            QLabel, QLineEdit, QComboBox { color: #f0f0f0; }
            QTableWidget { background: #3c3f41; gridline-color: #555; }
            QHeaderView::section { background: #444; color: #f0f0f0; }
            QPushButton { background: #555; color: #f0f0f0; border-radius:4px; padding:4px; }
        """)

    def apply_light_theme(self):
        self.setStyleSheet("")  # default
        self.setStyleSheet("""
            QMainWindow { background: #ffffff; color: #000000; }
            QLabel, QLineEdit, QComboBox { color: #000000; }
            QTableWidget { background: #f0f0f0; gridline-color: #ccc; }
            QHeaderView::section { background: #e0e0e0; color: #000000; }
            QPushButton { background: #d0d0d0; color: #000000; border-radius:4px; padding:4px; }
        """)