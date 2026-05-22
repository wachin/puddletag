# -*- coding: utf-8 -*-
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

DARK_STYLESHEET = """
QMainWindow, QDialog, QDockWidget {
    background-color: #2b2b2b;
    color: #efefef;
}
QWidget {
    background-color: #2b2b2b;
    color: #efefef;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox, QTableWidget {
    background-color: #3b3b3b;
    color: #efefef;
    border: 1px solid #555;
}
QPushButton {
    background-color: #4b4b4b;
    color: #efefef;
    border: 1px solid #555;
    padding: 5px;
}
QPushButton:hover {
    background-color: #5b5b5b;
}
QPushButton:pressed {
    background-color: #3b3b3b;
}
QHeaderView::section {
    background-color: #3b3b3b;
    color: #efefef;
    padding: 4px;
    border: 1px solid #555;
}
QTableWidget {
    gridline-color: #555;
}
QScrollBar:vertical {
    border: none;
    background: #2b2b2b;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #555;
    min-height: 20px;
}
QScrollBar:horizontal {
    border: none;
    background: #2b2b2b;
    height: 10px;
}
QScrollBar::handle:horizontal {
    background: #555;
    min-width: 20px;
}
QMenuBar, QMenu {
    background-color: #2b2b2b;
    color: #efefef;
}
QMenuBar::item:selected, QMenu::item:selected {
    background-color: #4b4b4b;
}
"""

def apply_dark_theme(app):
    app.setStyleSheet(DARK_STYLESHEET)
    
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(43, 43, 43))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(239, 239, 239))
    palette.setColor(QPalette.ColorRole.Base, QColor(59, 59, 59))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(43, 43, 43))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(239, 239, 239))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(239, 239, 239))
    palette.setColor(QPalette.ColorRole.Text, QColor(239, 239, 239))
    palette.setColor(QPalette.ColorRole.Button, QColor(43, 43, 43))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(239, 239, 239))
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(palette)

def apply_default_theme(app):
    app.setStyleSheet("")
    app.setPalette(app.style().standardPalette())

def update_theme(app, theme_name):
    if theme_name == "Dark Mode":
        apply_dark_theme(app)
    else:
        apply_default_theme(app)
