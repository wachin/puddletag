import unittest
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from puddlestuff.audioinfo import Tag
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

if __name__ == '__main__':
    unittest.main()
