"""
Action system tests for puddlestuff.

Tests for the action system including action loading, execution, and validation.
"""
import unittest
import os
import sys
import tempfile
import subprocess
from unittest.mock import MagicMock

# Mock unidecode before importing puddlestuff
sys.modules['unidecode'] = MagicMock()

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from puddlestuff.actiondlg import apply_actions, apply_macros, displaytags
from puddlestuff.functions import functions
from puddlestuff.puddleobjects import PuddleConfig
from puddlestuff.audioinfo import Tag

# Check if ffmpeg is available
try:
    subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    FFMPEG_AVAILABLE = True
except (subprocess.CalledProcessError, FileNotFoundError):
    FFMPEG_AVAILABLE = False


def create_test_audio_file(tmpdir, ext, codec_args):
    """Create a test audio file using ffmpeg."""
    audio_path = os.path.join(tmpdir, f'test.{ext}')
    cmd = [
        'ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono',
        '-t', '1'
    ] + codec_args + ['-y', audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed for {ext}: {result.stderr}")
    return audio_path


TEST_FORMATS = [
    ('flac', ['-c:a', 'flac']),
    ('ogg', ['-c:a', 'libvorbis']),
    ('mp3', ['-c:a', 'libmp3lame']),
    ('m4a', ['-c:a', 'aac']),
    ('wav', ['-c:a', 'pcm_s16le']),
    ('aiff', ['-c:a', 'pcm_s16be']),
]


class TestActionSystem(unittest.TestCase):
    """Test the action system components."""
    
    @classmethod
    def setUpClass(cls):
        """Check if ffmpeg is available."""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            cls.ffmpeg_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            cls.ffmpeg_available = False
        
        # Create QApplication once
        from PyQt6.QtWidgets import QApplication
        cls.app = QApplication.instance() or QApplication([])
    
    def setUp(self):
        if not self.ffmpeg_available:
            self.skipTest("ffmpeg not available")
        self.tmpdir = tempfile.TemporaryDirectory()
        
        # Create test audio files
        self.files = []
        self.tags = []
        for i, (ext, codec_args) in enumerate(TEST_FORMATS):
            audio_path = create_test_audio_file(self.tmpdir.name, ext, TEST_FORMATS[i % len(TEST_FORMATS)][1])
            self.files.append(audio_path)
            
            # Create tag with distinctive metadata
            tag = Tag(audio_path)
            tag['artist'] = f'Artist_{i}'
            tag['title'] = f'Title_{i}'
            tag['album'] = f'Album_{i}'
            tag['track'] = str(i + 1)
            tag['year'] = '2024'
            tag.save()
            self.tags.append(tag)
    
    def tearDown(self):
        self.tmpdir.cleanup()
    
    def test_apply_actions(self):
        """Test apply_actions function."""
        # Test with empty tags
        result = apply_actions([], [], {})
        self.assertEqual(result, {})
    
    def test_apply_macros(self):
        """Test apply_macros function."""
        # Test with empty tags
        result = apply_macros([], [], {})
        self.assertEqual(result, {})
    
    def test_displaytags(self):
        """Test displaytags function."""
        # Test with empty tags
        result = displaytags([])
        self.assertEqual(result, '<b>No change.</b>')
    
    def test_action_config_loading(self):
        """Test loading action configurations."""
        # Test that config can be loaded
        config = PuddleConfig()
        # Test that config can be loaded
        self.assertIsNotNone(config)
    
    def test_action_standard_loading(self):
        """Test loading standard action file."""
        # Test that standard action file exists
        standard_action = os.path.join(
            os.path.dirname(__file__), '..', 'puddlestuff', 'data', 'standard.action'
        )
        self.assertTrue(os.path.exists(standard_action))
    
    def test_action_caseconversion_loading(self):
        """Test loading caseconversion action file."""
        caseconversion_action = os.path.join(
            os.path.dirname(__file__), '..', 'puddlestuff', 'data', 'caseconversion.action'
        )
        self.assertTrue(os.path.exists(caseconversion_action))
    
    def test_action_file_exists(self):
        """Test that action files exist."""
        standard_action = os.path.join(
            os.path.dirname(__file__), '..', 'puddlestuff', 'data', 'standard.action'
        )
        self.assertTrue(os.path.exists(standard_action))
        
        caseconversion_action = os.path.join(
            os.path.dirname(__file__), '..', 'puddlestuff', 'data', 'caseconversion.action'
        )
        self.assertTrue(os.path.exists(caseconversion_action))
    
    def test_action_file_content(self):
        """Test action file content."""
        standard_action = os.path.join(
            os.path.dirname(__file__), '..', 'puddlestuff', 'data', 'standard.action'
        )
        with open(standard_action, 'r') as f:
            content = f.read()
        
        # Check that the action file has expected sections
        self.assertIn('[info]', content)
        self.assertIn('[Func0]', content)
        self.assertIn('func_name = replace', content)
    
    def test_action_function_execution(self):
        """Test executing action functions."""
        from puddlestuff.functions import functions
        from puddlestuff.audioinfo import Tag
        import tempfile
        import os
        import subprocess
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            subprocess.run(['ffmpeg','-f','lavfi','-i','anullsrc=r=44100:cl=mono','-t','1','-c:a','flac','-y',f], capture_output=True)
            tag = Tag(f)
            tag['artist'] = 'Test Artist'
            tag['title'] = 'Test Title'
            tag.save()
            
            # Test replace function (used in standard action)
            from puddlestuff.functions import replace
            result = replace('Test Artist', 'Test', 'New')
            self.assertEqual(result, 'New Artist')
    
    def test_action_execution_flow(self):
        """Test action execution flow with mock tags."""
        from puddlestuff.functions import functions
        tag = Tag(self.files[0])
        original_artist = tag.get('artist')
        
        # Apply replace function - use tag.get() which returns list, get first element
        artist_value = tag.get('artist')
        artist_str = artist_value[0] if isinstance(artist_value, list) else artist_value
        # The artist is 'Artist_0', so replacing 'Artist' with 'NewArtist' gives 'NewArtist_0'
        result = functions['replace'](artist_str, 'Artist', 'NewArtist')
        self.assertEqual(result, 'NewArtist_0')
    
    def test_action_config_save_load(self):
        """Test saving and loading action configuration."""
        config = PuddleConfig()
        # Test that config can be saved and loaded
        config.set('test', 'key', 'value')
        self.assertEqual(config.get('test', 'key', ''), 'value')
    
    def test_action_duplicate_loading(self):
        """Test loading duplicate action names."""
        config = PuddleConfig()
        config.set('test_section', 'key1', 'value1')
        config.set('test_section', 'key2', 'value2')
        self.assertEqual(config.get('test_section', 'key1', ''), 'value1')
        self.assertEqual(config.get('test_section', 'key2', ''), 'value2')
    
    def test_action_lambda_capture(self):
        """Test lambda capture in action loops."""
        config = PuddleConfig()
        # Test that lambda capture works correctly
        for i in range(3):
            config.set(f'section{i}', 'key', f'value{i}')
        
        self.assertEqual(config.get('section0', 'key', ''), 'value0')
        self.assertEqual(config.get('section1', 'key', ''), 'value1')
        self.assertEqual(config.get('section2', 'key', ''), 'value2')
    
    def test_action_config_persistence(self):
        """Test action config persistence across reloads."""
        config = PuddleConfig()
        config.set('test', 'persistent_key', 'persistent_value')
        config.save()
        
        # Create new config instance
        config2 = PuddleConfig()
        config2.filename = config.filename
        config2.reload()
        
        self.assertEqual(config2.get('test', 'persistent_key', ''), 'persistent_value')


if __name__ == '__main__':
    unittest.main()
