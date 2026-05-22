# -*- coding: utf-8 -*-
import unittest
import os
import sys
from unittest.mock import MagicMock

# Mock unidecode
sys.modules['unidecode'] = MagicMock()

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from puddlestuff.mainwin.statistics import StatisticsDialog
from PyQt6.QtWidgets import QApplication

app = QApplication([])

class MockTrack(dict):
    def __init__(self, data):
        super().__init__(data)
    
    def get(self, key, default=None):
        return super().get(key, default)

class TestStatistics(unittest.TestCase):
    def test_statistics_calculation(self):
        tracks = [
            MockTrack({'genre': ['Rock'], '__size': 1000, '__length': '03:00', '__ext': 'mp3', '__bitrate': '128 kb/s'}),
            MockTrack({'genre': ['Pop'], '__size': 2000, '__length': '04:00', '__ext': 'flac', '__bitrate': '900 kb/s'}),
            MockTrack({'genre': ['Rock'], '__size': 1500, '__length': '03:30', '__ext': 'mp3', '__bitrate': '192 kb/s'})
        ]
        
        dialog = StatisticsDialog(tracks=tracks)
        # We can't easily test the UI, but we can check if it initializes without error
        self.assertEqual(len(dialog.tracks), 3)

if __name__ == '__main__':
    unittest.main()
