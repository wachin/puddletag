import os

from PyQt6.QtWidgets import QDialog, QHBoxLayout, QPushButton, QTextEdit, QVBoxLayout

from ..constants import LOG_FILENAME
from ..translations import translate


class LogDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translate("Logs", "Application Logs"))
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout(self)

        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        layout.addWidget(self.log_edit)

        self.refresh_log()

        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton(translate("Logs", "Refresh"))
        refresh_btn.clicked.connect(self.refresh_log)

        clear_btn = QPushButton(translate("Logs", "Clear Log File"))
        clear_btn.clicked.connect(self.clear_log)

        close_btn = QPushButton(translate("Defaults", "Close"))
        close_btn.clicked.connect(self.accept)

        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def refresh_log(self):
        if os.path.exists(LOG_FILENAME):
            try:
                with open(LOG_FILENAME, "r", encoding="utf-8") as f:
                    self.log_edit.setPlainText(f.read())
                    # Scroll to bottom
                    self.log_edit.verticalScrollBar().setValue(
                        self.log_edit.verticalScrollBar().maximum()
                    )
            except OSError as e:
                self.log_edit.setPlainText(f"Error reading log: {e}")
        else:
            self.log_edit.setPlainText("Log file does not exist.")

    def clear_log(self):
        if os.path.exists(LOG_FILENAME):
            try:
                with open(LOG_FILENAME, "w", encoding="utf-8") as f:
                    f.write("")
                self.refresh_log()
            except OSError as e:
                self.log_edit.setPlainText(f"Error clearing log: {e}")


def show_logs(parent):
    dialog = LogDialog(parent)
    dialog.exec()
