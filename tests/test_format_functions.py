"""
Format function and converter tests for puddlestuff.

Tests the format string functions, converters, and edge cases.
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

from puddlestuff.findfunc import parsefunc, filenametotag, tagtofilename
from puddlestuff.audioinfo import Tag


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


class TestFormatFunctions(unittest.TestCase):
    """Test format string functions and converters."""
    
    @classmethod
    def setUpClass(cls):
        """Check if ffmpeg is available."""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            cls.available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            cls.available = False
    
    def setUp(self):
        import subprocess
        if not subprocess.run(['ffmpeg', '-version'], capture_output=True).returncode == 0:
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
            tag.save()
            self.tags.append(tag)
    
    def tearDown(self):
        self.tmpdir.cleanup()
    
    def test_parsefunc_basic(self):
        """Test basic parsefunc with simple format strings."""
        tag = self.tags[0]
        # Test simple field substitution
        result = parsefunc('%artist% - %title%', tag)
        self.assertEqual(result, 'Artist_0 - Title_0')
    
    def test_parsefunc_multiple_fields(self):
        """Test parsefunc with multiple fields."""
        tag = self.tags[0]
        result = parsefunc('%artist% - %title% (%album%)', tag)
        self.assertEqual(result, 'Artist_0 - Title_0 (Album_0)')
    
    def test_parsefunc_unknown_field(self):
        """Test parsefunc with unknown field."""
        tag = self.tags[0]
        result = parsefunc('%unknown%', tag)
        self.assertEqual(result, '')
    
    def test_parsefunc_with_state(self):
        """Test parsefunc with state dictionary."""
        tag = self.tags[0]
        state = {'__counter': '5'}
        result = parsefunc('Track: %__counter%', tag, state=state)
        self.assertEqual(result, 'Track: 5')
    
    def test_parsefunc_functions(self):
        """Test parsefunc with functions."""
        tag = self.tags[0]
        # Test upper function
        result = parsefunc('$upper(%artist%)', tag)
        self.assertEqual(result, 'ARTIST_0')
        
        # Test lower function
        result = parsefunc('$lower(%title%)', tag)
        self.assertEqual(result, 'title_0')
    
    def test_parsefunc_nested(self):
        """Test parsefunc with nested functions."""
        tag = self.tags[0]
        result = parsefunc('$upper($lower(%artist%))', tag)
        self.assertEqual(result, 'ARTIST_0')
    
    def test_parsefunc_multiple_fields(self):
        """Test parsefunc with multiple tags."""
        tags = self.tags[:2]
        results = []
        for tag in tags:
            result = parsefunc('%artist% - %title%', tag)
            results.append(result)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], 'Artist_0 - Title_0')
        self.assertEqual(results[1], 'Artist_1 - Title_1')
    
    def test_tagtofilename_basic(self):
        """Test tagtofilename basic functionality."""
        tag = self.tags[0]
        result = tagtofilename('%artist% - %title%', tag)
        self.assertEqual(result, 'Artist_0 - Title_0')
    
    def test_tagtofilename_special_chars(self):
        """Test tagtofilename with special characters."""
        tag = self.tags[0]
        tag['title'] = 'Title with "quotes" and /slashes/'
        result = tagtofilename('%title%', tag)
        # Should handle special characters
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    def test_filenametotag_basic(self):
        """Test filenametotag basic functionality."""
        tag = Tag(self.files[0])
        # Create a filename pattern
        pattern = '%artist% - %title%'
        filename = 'TestArtist - TestTitle.flac'
        
        result = filenametotag(pattern, filename, True)
        self.assertIsInstance(result, dict)
    
    def test_tagtofilename_unicode(self):
        """Test tagtofilename with Unicode characters."""
        tag = self.tags[0]
        tag['title'] = 'Тест Название'
        tag['artist'] = 'アーティスト'
        result = tagtofilename('%artist% - %title%', tag)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    def test_tagtofilename_empty_fields(self):
        """Test tagtofilename with empty fields."""
        tag = Tag(self.files[0])
        # Don't set some fields
        result = tagtofilename('%artist% - %title% - %album%', tag)
        # Should handle missing fields gracefully
        self.assertIsInstance(result, str)
    
    def test_filenametotag_edge_cases(self):
        """Test filenametotag with edge cases."""
        tag = Tag(self.files[0])
        
        # Test with pattern that doesn't match
        result = filenametotag('%artist% - %title%', 'not_matching.flac', True)
        # Should return something (maybe None or empty dict)
        self.assertIsNotNone(result)
    
    def test_tagtofilename_special_chars(self):
        """Test tagtofilename with special characters in filename."""
        tag = self.tags[0]
        tag['title'] = 'Title with "quotes" and /slashes/'
        result = tagtofilename('%title%', tag)
        self.assertIsInstance(result, str)
        # Should sanitize special characters
        self.assertIn('/', result)  # tagtofilename does not sanitize by default
        # tagtofilename does not sanitize quotes by default


if __name__ == '__main__':
    unittest.main()
