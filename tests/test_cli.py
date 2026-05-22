import unittest
import os
import sys
from unittest.mock import MagicMock

# Mock unidecode
sys.modules['unidecode'] = MagicMock()

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from puddlestuff.cli import cli_export, cli_tag

class TestCLI(unittest.TestCase):
    def test_cli_export_help(self):
        # This is more of a smoke test to ensure imports work
        self.assertTrue(callable(cli_export))
        self.assertTrue(callable(cli_tag))

if __name__ == '__main__':
    unittest.main()
