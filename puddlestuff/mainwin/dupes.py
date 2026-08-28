from collections import defaultdict

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from ..translations import translate


class DuplicateFinderDialog(QDialog):
    def __init__(self, parent=None, tracks=None):
        super().__init__(parent)
        self.tracks = tracks
        self.setWindowTitle(translate("Dupes", "Duplicate Finder"))
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout(self)

        # Criteria selection
        layout.addWidget(
            QLabel(f"<b>{translate('Dupes', 'Select fields to compare:')}</b>")
        )
        criteria_layout = QHBoxLayout()
        self.artist_cb = QCheckBox(translate("Dupes", "Artist"))
        self.artist_cb.setChecked(True)
        self.title_cb = QCheckBox(translate("Dupes", "Title"))
        self.title_cb.setChecked(True)
        self.album_cb = QCheckBox(translate("Dupes", "Album"))
        self.length_cb = QCheckBox(translate("Dupes", "Duration"))

        criteria_layout.addWidget(self.artist_cb)
        criteria_layout.addWidget(self.title_cb)
        criteria_layout.addWidget(self.album_cb)
        criteria_layout.addWidget(self.length_cb)
        layout.addLayout(criteria_layout)

        find_btn = QPushButton(translate("Dupes", "Find Duplicates"))
        find_btn.clicked.connect(self.find_duplicates)
        layout.addWidget(find_btn)

        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(
            [
                translate("Dupes", "Artist"),
                translate("Dupes", "Title"),
                translate("Dupes", "Album"),
                translate("Dupes", "Path"),
            ]
        )
        self.results_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.results_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        layout.addWidget(self.results_table)

        # Actions
        btn_layout = QHBoxLayout()
        self.select_btn = QPushButton(translate("Dupes", "Select in Main Window"))
        self.select_btn.clicked.connect(self.select_in_main)
        self.select_btn.setEnabled(False)

        close_btn = QPushButton(translate("Defaults", "Close"))
        close_btn.clicked.connect(self.accept)

        btn_layout.addWidget(self.select_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self.duplicate_groups = []

    def find_duplicates(self):
        fields = []
        if self.artist_cb.isChecked():
            fields.append("artist")
        if self.title_cb.isChecked():
            fields.append("title")
        if self.album_cb.isChecked():
            fields.append("album")
        if self.length_cb.isChecked():
            fields.append("__length")

        if not fields:
            return

        groups = defaultdict(list)
        for t in self.tracks:
            key = []
            for f in fields:
                val = t.get(f, [""])[0] if isinstance(t.get(f), list) else t.get(f, "")
                key.append(str(val).lower().strip())
            groups[tuple(key)].append(t)

        self.duplicate_groups = [g for g in groups.values() if len(g) > 1]
        self.display_results()

    def display_results(self):
        self.results_table.setRowCount(0)
        row = 0
        for group in self.duplicate_groups:
            for t in group:
                self.results_table.insertRow(row)
                self.results_table.setItem(
                    row, 0, QTableWidgetItem(str(t.get("artist", [""])[0]))
                )
                self.results_table.setItem(
                    row, 1, QTableWidgetItem(str(t.get("title", [""])[0]))
                )
                self.results_table.setItem(
                    row, 2, QTableWidgetItem(str(t.get("album", [""])[0]))
                )
                self.results_table.setItem(row, 3, QTableWidgetItem(t.filepath))
                # Store track object in the first item
                self.results_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, t)
                row += 1
            # Add a separator row or visual break? For now just alternating colors might help or groups

        self.select_btn.setEnabled(len(self.duplicate_groups) > 0)

    def select_in_main(self):
        selected_rows = self.results_table.selectionModel().selectedRows()
        if not selected_rows:
            return

        selected_tracks = []
        for index in selected_rows:
            track = self.results_table.item(index.row(), 0).data(
                Qt.ItemDataRole.UserRole
            )
            selected_tracks.append(track)

        if selected_tracks:
            # We need to tell the main window to select these tracks
            from . import funcs

            # This is a bit tricky as we need to find the rows in the main table
            # But we can use funcs.status['table']
            table = funcs.status["table"]
            model = table.model()

            table.clearSelection()
            for t in selected_tracks:
                for row in range(model.rowCount()):
                    if model.taginfo[row] == t:
                        table.selectRow(row)
                        break
            self.accept()


def show_dupe_finder(parent, tracks):
    dialog = DuplicateFinderDialog(parent, tracks)
    dialog.exec()
