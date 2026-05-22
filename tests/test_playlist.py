import unittest
import os
import sys
from unittest.mock import MagicMock

# Mock unidecode
sys.modules['unidecode'] = MagicMock()

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from puddlestuff.m3u import auto_update_playlist
from puddlestuff.puddleobjects import PuddleConfig
from puddlestuff.puddletag import status

class MockTag(dict):
    def __init__(self, filepath, artist, title):
        super().__init__({'artist': artist, 'title': title})
        self.filepath = filepath
        self.length = 180
    
    def get(self, key, default=None):
        return super().get(key, default)

class TestPlaylist(unittest.TestCase):
    def setUp(self):
        # Mock PuddleConfig
        self.config_mock = MagicMock()
        self.patcher = unittest.mock.patch('puddlestuff.m3u.PuddleConfig', return_value=self.config_mock)
        self.patcher.start()
        
        self.config_mock.get.side_effect = lambda s, k, d: {
            ('playlist', 'auto_update'): True,
            ('playlist', 'filepattern'): 'puddletag.m3u',
            ('playlist', 'extinfo'): True,
            ('playlist', 'extpattern'): '%artist% - %title%',
            ('playlist', 'reldir'): False,
            ('playlist', 'windows_separator'): False,
        }.get((s, k), d)
        
    def tearDown(self):
        self.patcher.stop()
        
    def test_auto_update_playlist(self):
        # Create a temp dir
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = os.path.join(tmpdir, "test1.mp3")
            tag1 = MockTag(file1, "Artist 1", "Title 1")
            
            # Mock status['alltags']
            status['alltags'] = [tag1]
            
            # Run auto update
            auto_update_playlist([tag1])
            
            # Check if playlist was created
            playlist_path = os.path.join(tmpdir, "puddletag.m3u")
            self.assertTrue(os.path.exists(playlist_path))
            
            with open(playlist_path, 'r') as f:
                content = f.read()
                self.assertIn("test1.mp3", content)
                self.assertIn("#EXTM3U", content)

if __name__ == '__main__':
    unittest.main()
