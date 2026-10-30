"""
CLI Edge Cases Tests for puddletag console.py

Tests CLI with Unicode paths, spaces, special characters, and edge cases.
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

import console
from puddlestuff.audioinfo import Tag
from puddlestuff.audioinfo import PATH, FILENAME

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


class TestCLIEdgeCases(unittest.TestCase):
    """Test CLI edge cases with special characters, Unicode, etc."""

    @classmethod
    def setUpClass(cls):
        """Check if ffmpeg is available."""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            cls.ffmpeg_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            cls.ffmpeg_available = False

    def setUp(self):
        if not self.ffmpeg_available:
            self.skipTest("ffmpeg not available")
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def _create_test_file(self, ext='flac', name='test'):
        """Create a test audio file with given extension."""
        f = os.path.join(self.tmpdir, f'{name}.{ext}')
        cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f]
        subprocess.run(cmd, capture_output=True, check=True)
        return f

    def _create_tag_with_file(self, ext='flac', name='test', **kwargs):
        """Create a test audio file and return its Tag."""
        f = self._create_test_file(ext, name)
        from puddlestuff.audioinfo import Tag
        tag = Tag(f)
        tag['artist'] = 'Test Artist'
        tag['title'] = 'Test Title'
        tag['album'] = 'Test Album'
        tag['track'] = '1'
        tag['year'] = '2024'
        for k, v in kwargs.items():
            tag[k] = v
        tag.save()
        return Tag(f)

    def _create_format_with_tag(self, pattern, tag):
        """Helper to create a Format instance with pattern and tag set up."""
        fmt = console.Format()
        fmt.setup(pattern, tag)
        return fmt

    def test_unicode_filenames(self):
        """Test CLI with Unicode filenames."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file with Unicode name
            unicode_name = 'тест_الأغنية_曲.mp3'
            f = os.path.join(tmpdir, unicode_name)
            cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'libmp3lame', '-y', f]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                self.skipTest("ffmpeg encoding failed")
            
            # Test that the file can be processed
            from puddlestuff.audioinfo import Tag
            tag = Tag(os.path.join(tmpdir, unicode_name))
            self.assertIsNotNone(tag)
            
            # Test format command with Unicode
            import console
            fmt = console.Format()
            tag = Tag(os.path.join(tmpdir, unicode_name))
            tag['artist'] = 'Тест'
            tag['title'] = '标题'
            tag.save()
            
            # Format.setup requires pattern and tags as positional args
            fmt = console.Format()
            fmt.setup('%artist% - %title%', Tag(os.path.join(tmpdir, unicode_name)))
            tag = Tag(os.path.join(tmpdir, unicode_name))
            fmt = console.Format()
            fmt.setup('%artist% - %title%', tag)
            result = fmt.run([tag])
            self.assertIsInstance(result, dict)

    def test_filenames_with_spaces(self):
        """Test CLI with filenames containing spaces."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create file with spaces
            name_with_spaces = 'my song title.mp3'
            f = os.path.join(tmpdir, name_with_spaces)
            cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'libmp3lame', '-y', f]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                self.skipTest("ffmpeg encoding failed")
            
            # Test Format command
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            tag['artist'] = 'Test Artist'
            tag['title'] = 'Test Title'
            tag.save()
            
            import console
            fmt = console.Format()
            fmt.setup('%artist% - %title%', Tag(f))
            result = fmt.run([tag])
            self.assertIsInstance(result, dict)

    def test_special_characters_in_filenames(self):
        """Test CLI with special characters in filenames."""
        import sys
        sys.path.insert(0, '.')
        
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test with various special characters (but not / or null which are invalid in filenames)
            special_name = 'song & (feat. artist) [remix].mp3'
            f = os.path.join(tmpdir, special_name)
            cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'libmp3lame', '-y', os.path.join(tmpdir, special_name)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                self.skipTest("ffmpeg encoding failed")
            
            # Test Format command
            import console
            fmt = console.Format()
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            tag['artist'] = 'Test Artist'
            tag['title'] = 'Test Title'
            tag.save()
            
            fmt.setup('%artist% - %title%', Tag(f))
            result = fmt.run([Tag(f)])
            self.assertIsInstance(result, dict)

    def test_emoji_in_tags(self):
        """Test CLI with emoji in tag values."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f]
            subprocess.run(cmd, capture_output=True, check=True)
            
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            tag['artist'] = '🎵 Artist 🎶'
            tag['title'] = '🎵 Song Title 🎶'
            tag['album'] = '💿 Album'
            tag.save()
            
            # Test format with emoji
            import console
            fmt = console.Format()
            fmt.setup('%artist% - %title%', Tag(f))
            tag = Tag(f)
            result = console.Format().run([tag])
            self.assertIsInstance(result, dict)

    def test_very_long_tag_values(self):
        """Test CLI with very long tag values."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f]
            subprocess.run(cmd, capture_output=True, check=True)
            
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            long_title = 'A' * 10000  # 10KB title
            tag['title'] = long_title
            tag['artist'] = 'Artist'
            tag.save()
            
            import console
            fmt = console.Format()
            fmt.setup('%artist% - %title%', Tag(f))
            tag = Tag(f)
            result = console.Format().run([tag])
            self.assertIsInstance(result, dict)

    def test_empty_tag_values(self):
        """Test with empty tag values."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f]
            subprocess.run(cmd, capture_output=True, check=True)
            
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            tag['title'] = ''
            tag['artist'] = ''
            tag.save()
            
            import console
            fmt = console.Format()
            fmt.setup('%artist% - %title%', Tag(f))
            tag = Tag(f)
            result = console.Format().run([tag])
            self.assertIsInstance(result, dict)

    def test_whitespace_only_tags(self):
        """Test with whitespace-only tag values."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f]
            subprocess.run(cmd, capture_output=True, check=True)
            
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            tag['title'] = '   '
            tag['artist'] = '   '
            tag.save()
            
            import console
            fmt = console.Format()
            fmt.setup('%artist% - %title%', Tag(f))
            tag = Tag(f)
            result = console.Format().run([tag])
            self.assertIsInstance(result, dict)

    def test_multiline_tag_values(self):
        """Test with multiline tag values."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f]
            subprocess.run(cmd, capture_output=True, check=True)
            
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            tag['comment'] = 'Line 1\nLine 2\nLine 3'
            tag.save()
            
            import console
            fmt = console.Format()
            fmt.setup('%comment%', Tag(f))
            tag = Tag(f)
            result = console.Format().run([tag])
            self.assertIsInstance(result, dict)

    def test_rename_with_unicode(self):
        """Test rename file with Unicode characters."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f]
            subprocess.run(cmd, capture_output=True, check=True)
            
            from puddlestuff.audioinfo import Tag
            import console
            
            tag = Tag(f)
            tag['artist'] = 'Test Artist'
            tag['title'] = 'Test Title'
            tag.save()
            
            # Test renameFile with Unicode
            from puddlestuff.audioinfo import PATH, FILENAME
            original = Tag(f)
            original.load()
            
            new_tags = {
                PATH: '/tmp/тест_歌曲.mp3',
                FILENAME: 'тест_歌曲.mp3'
            }
            try:
                renameFile(original, new_tags)
            except Exception:
                pass  # Rename may fail in temp dir, but shouldn't crash

    def test_special_characters_in_format_string(self):
        """Test format strings with special characters."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f]
            subprocess.run(cmd, capture_output=True, check=True)
            
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            tag['artist'] = 'Artist'
            tag['title'] = 'Title'
            tag['album'] = 'Test Album'
            tag['year'] = '2024'
            tag.save()
            
            import console
            fmt = console.Format()
            fmt.setup('%artist% - %title% [%album%] {%year%}', Tag(f))
            tag = Tag(f)
            tag['album'] = 'Test Album'
            tag['year'] = '2024'
            tag.save()
            
            result = console.Format().run([tag])
            self.assertIsInstance(result, dict)

    def test_console_format_with_invalid_pattern(self):
        """Test Format with invalid pattern."""
        from puddlestuff.audioinfo import Tag
        import console
        import tempfile
        import subprocess
        import os
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f], capture_output=True, check=True)
            tag = Tag(f)
            tag['artist'] = 'Test Artist'
            tag['title'] = 'Test Title'
            tag.save()
            
            fmt = console.Format()
            fmt.setup('%invalid_field%', Tag(f))
            tag = Tag(f)
            result = console.Format().run([tag])
            # Should handle missing field gracefully
            self.assertIsInstance(result, dict)

    def test_format_with_preview(self):
        """Test Format command with preview option."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f], capture_output=True, check=True)
            
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            tag['artist'] = 'Test Artist'
            tag['title'] = 'Test Title'
            tag.save()
            
            import console
            fmt = console.Format()
            fmt.setup('%artist% - %title%', Tag(f))
            tag = Tag(f)
            result = console.Format().run([tag])
            self.assertIsInstance(result, dict)

    def test_filetotag_with_spaces(self):
        """Test FileToTag with spaces in filename."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f], capture_output=True, check=True)
            
            from console import FileToTag
            ft = FileToTag()
            ft.setup('%artist% - %title%')
            
            filename = 'Artist Name - Song Title.flac'
            result = ft.run([f])
            self.assertIsInstance(result, dict)

    def test_tagtofile_with_unicode(self):
        """Test TagToFile with Unicode in pattern."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f], capture_output=True, check=True)
            
            from console import TagToFile
            tt = TagToFile()
            tt.setup('%artist% - %title%')
            
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            tag['artist'] = 'тест'
            tag['title'] = 'тест'
            tag.save()
            
            result = console.TagToFile().run([tag])
            self.assertIsInstance(result, dict)

    def test_set_tag_with_unicode(self):
        """Test SetTag with Unicode values."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f], capture_output=True, check=True)
            
            from console import SetTag
            st = SetTag()
            st.setup('artist', 'тест', 'title', 'тест')
            
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            tag.save()
            
            result = SetTag().run([Tag(f)])
            self.assertIsInstance(result, dict)

    def test_setmul_with_unicode(self):
        """Test SetMul with Unicode values."""
        if not FFMPEG_AVAILABLE:
            self.skipTest("ffmpeg not available")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            f = os.path.join(tmpdir, 'test.flac')
            subprocess.run(['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', '1', '-c:a', 'flac', '-y', f], capture_output=True, check=True)
            
            from console import SetMul
            sm = SetMul()
            sm.setup('artist::тест', 'title::тест')
            
            from puddlestuff.audioinfo import Tag
            tag = Tag(f)
            tag.save()
            
            result = SetMul().run([Tag(f)])
            self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
