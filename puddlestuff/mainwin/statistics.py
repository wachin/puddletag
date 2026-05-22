# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QPushButton)
from PyQt6.QtCore import Qt
from ..translations import translate
from .. import audioinfo
from collections import Counter

class StatisticsDialog(QDialog):
    def __init__(self, parent=None, tracks=None):
        super(StatisticsDialog, self).__init__(parent)
        self.tracks = tracks
        self.setWindowTitle(translate("Statistics", "Library Statistics"))
        self.setMinimumSize(500, 600)
        
        layout = QVBoxLayout(self)
        
        # General Info
        info_layout = QVBoxLayout()
        total_tracks = len(tracks)
        total_size = sum(int(t.get('__size', 0)) for t in tracks)
        total_length = sum(audioinfo.util.lnglength(t.get('__length', '00:00')) for t in tracks)
        
        info_layout.addWidget(QLabel(f"<b>{translate('Statistics', 'Total Tracks:')}</b> {total_tracks}"))
        info_layout.addWidget(QLabel(f"<b>{translate('Statistics', 'Total Size:')}</b> {audioinfo.util.str_filesize(total_size)}"))
        info_layout.addWidget(QLabel(f"<b>{translate('Statistics', 'Total Duration:')}</b> {audioinfo.util.strlength(total_length)}"))
        layout.addLayout(info_layout)
        
        # Genre Distribution
        layout.addWidget(QLabel(f"<h3>{translate('Statistics', 'Genre Distribution')}</h3>"))
        self.genre_table = QTableWidget()
        self.populate_table(self.genre_table, 'genre')
        layout.addWidget(self.genre_table)
        
        # Format Distribution
        layout.addWidget(QLabel(f"<h3>{translate('Statistics', 'Format Distribution')}</h3>"))
        self.format_table = QTableWidget()
        self.populate_table(self.format_table, '__ext')
        layout.addWidget(self.format_table)
        
        # Bitrate Distribution
        layout.addWidget(QLabel(f"<h3>{translate('Statistics', 'Bitrate Distribution')}</h3>"))
        self.bitrate_table = QTableWidget()
        self.populate_table(self.bitrate_table, '__bitrate')
        layout.addWidget(self.bitrate_table)
        
        close_btn = QPushButton(translate("Defaults", "Close"))
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def populate_table(self, table, field):
        data = []
        for t in self.tracks:
            val = t.get(field, ['Unknown'])
            if isinstance(val, list):
                if val:
                    data.append(str(val[0]))
                else:
                    data.append('Unknown')
            else:
                data.append(str(val))
        
        counts = Counter(data)
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        
        table.setColumnCount(2)
        table.setRowCount(len(sorted_counts))
        table.setHorizontalHeaderLabels([translate("Statistics", "Value"), translate("Statistics", "Count")])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        for i, (val, count) in enumerate(sorted_counts):
            table.setItem(i, 0, QTableWidgetItem(val))
            table.setItem(i, 1, QTableWidgetItem(str(count)))

def show_statistics(parent, tracks):
    dialog = StatisticsDialog(parent, tracks)
    dialog.exec()
