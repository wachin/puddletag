import unittest
import os
import sys
from unittest.mock import MagicMock

# Mock unidecode before importing puddlestuff
mock_unidecode = MagicMock()
sys.modules['unidecode'] = mock_unidecode

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from puddlestuff.export import ExportDialog
from PyQt6.QtWidgets import QApplication

app = QApplication([])

class MockTrack(dict):
    def get(self, key, default=None):
        return super().get(key, default)

class TestExport(unittest.TestCase):
    def test_process_template_no_loop(self):
        tracks = [
            MockTrack({'artist': 'Artist 1', 'title': 'Title 1'}),
            MockTrack({'artist': 'Artist 2', 'title': 'Title 2'})
        ]
        dialog = ExportDialog(tracks=tracks)
        template = "%artist% - %title%"
        result = dialog.process_template(template, tracks)
        self.assertEqual(result, "Artist 1 - Title 1\nArtist 2 - Title 2\n")

    def test_process_template_with_loop(self):
        tracks = [
            MockTrack({'artist': 'Artist B', 'title': 'Title 2'}),
            MockTrack({'artist': 'Artist A', 'title': 'Title 1'})
        ]
        dialog = ExportDialog(tracks=tracks)
        template = "Header\n$loop(%artist%)%artist% - %title%\n$loopend()Footer"
        result = dialog.process_template(template, tracks)
        # Sorts by artist, so Artist A should come first
        self.assertIn("Artist A - Title 1\nArtist B - Title 2\n", result)
        self.assertTrue(result.startswith("Header"))
        self.assertTrue(result.endswith("Footer"))

if __name__ == '__main__':
    unittest.main()
