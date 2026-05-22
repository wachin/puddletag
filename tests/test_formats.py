import unittest
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from puddlestuff.audioinfo import Tag
from puddlestuff.audioinfo.formats import iter_supported_formats, supported_formats_rst
from puddlestuff.audioinfo.id3 import WAVEFileType, AACFileType, AIFFFileType
from puddlestuff.audioinfo.apev2 import MonkeysAudio

class TestAudioFormats(unittest.TestCase):
    def test_format_registration(self):
        # This test checks if the new formats are correctly registered in the tagging engine
        from puddlestuff.audioinfo import tag_modules
        
        registered_extensions = []
        for m in tag_modules:
            if hasattr(m, 'filetypes'):
                for ftype in m.filetypes:
                    if len(ftype) > 3:
                        exts = ftype[3]
                        if isinstance(exts, list):
                            registered_extensions.extend(exts)
                        else:
                            registered_extensions.append(exts)
        
        # Check for our newly added formats
        self.assertIn('wav', registered_extensions)
        self.assertIn('aac', registered_extensions)
        self.assertIn('aiff', registered_extensions)
        self.assertIn('dsf', registered_extensions)
        self.assertIn('tak', registered_extensions)
        self.assertIn('tta', registered_extensions)
        self.assertIn('ofr', registered_extensions)

    def test_supported_formats_documentation_uses_registered_formats(self):
        rows = list(iter_supported_formats())
        documented_extensions = {
            extension
            for _tag_format, _audio_format, extensions in rows
            for extension in extensions
        }

        self.assertIn(('VorbisComment', 'Ogg Opus', ('opus', 'opus.ogg')), rows)
        self.assertIn(('MP4', 'MP4', ('m4a', 'm4v', 'mp4')), rows)
        self.assertIn('wav', documented_extensions)
        self.assertIn('tta', documented_extensions)
        self.assertIn('ofr', documented_extensions)

    def test_supported_formats_rst_is_generated_from_registry(self):
        rst = supported_formats_rst()

        self.assertIn('Supported formats:', rst)
        self.assertIn('MP4 (MP4: m4a, m4v, mp4)', rst)
        self.assertIn('Ogg Opus (VorbisComment: opus, opus.ogg)', rst)
        self.assertTrue(rst.endswith('.\n'))

if __name__ == '__main__':
    unittest.main()
