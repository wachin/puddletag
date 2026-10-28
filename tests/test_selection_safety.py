"""
Selection and Model Safety Tests

Tests for verifying that selection and model operations correctly preserve
the mapping between visual rows and underlying audio files after:
- Filtering
- Sorting
- Reloading
- Folder changes
"""

import unittest
import os
import sys
import tempfile
import subprocess
from unittest.mock import MagicMock, patch

# Mock unidecode before importing puddlestuff
sys.modules['unidecode'] = MagicMock()

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from puddlestuff.tagmodel import TagTable, TagModel
from puddlestuff.audioinfo import Tag
from puddlestuff.puddletag import status
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest


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


# Test formats that can be created with ffmpeg
TEST_FORMATS = [
    ('flac', ['-c:a', 'flac']),
    ('ogg', ['-c:a', 'libvorbis']),
    ('mp3', ['-c:a', 'libmp3lame']),
    ('m4a', ['-c:a', 'aac']),
    ('wav', ['-c:a', 'pcm_s16le']),
]


class MockAudioFile(dict):
    """A simple mock for audio files that works with TagModel."""
    def __init__(self, filepath, artist, title, album='Test Album', track='1', year='2024'):
        super().__init__()
        self.filepath = filepath
        self.update({
            'artist': [artist],
            'title': [title],
            'album': [album],
            'track': [track],
            'year': [year],
        })
        self.length = 180
        self.preview = {}
        self.undo = {}
        self.previewundo = {}
        self.color = None
        self._temp = {}
        self.library = None
        self.dirpath = os.path.dirname(filepath)
        self.filename = os.path.basename(filepath)
        self.ext = os.path.splitext(filepath)[1][1:]
        # Required for audio_filter
        self.mapping = {}
        self.revmapping = {}
        # Required for write()
        self.accessed = None
        self.modified = None
    
    def get(self, key, default=None):
        return super().get(key, default)
    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
    
    def __contains__(self, key):
        return super().__contains__(key)
    
    def items(self):
        return super().items()
    
    def keys(self):
        return super().keys()
    
    def values(self):
        return super().values()
    
    def update(self, other):
        if hasattr(other, 'items'):
            super().update(other.items())
        else:
            for k, v in other:
                self[k] = v
    
    def clear(self):
        super().clear()

    def save(self, library=False):
        pass

    def realvalue(self, key, default=None):
        return self.get(key, default)


class TestSelectionModelSafety(unittest.TestCase):
    """Test that selection and model operations preserve correct file mapping."""
    
    @classmethod
    def setUpClass(cls):
        """Check if ffmpeg is available."""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            cls.ffmpeg_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            cls.ffmpeg_available = False
        
        # Create QApplication once
        cls.app = QApplication.instance() or QApplication([])
    
    def setUp(self):
        if not self.ffmpeg_available:
            self.skipTest("ffmpeg not available")
        
        # Create temp directory with test files
        self.tmpdir = tempfile.TemporaryDirectory()
        
        # Create test audio files with distinct metadata
        self.files = []
        self.audio_tags = []
        
        for i, (ext, codec_args) in enumerate(TEST_FORMATS):
            audio_path = create_test_audio_file(self.tmpdir.name, ext, codec_args)
            
            # Create mock tag with distinct metadata
            tag = MockAudioFile(
                filepath=audio_path,
                artist=f'TestArtist{i}',
                title=f'TestTitle{i}',
                album=f'TestAlbum{i}',
                track=str(i + 1),
                year='2024'
            )
            # Add mapping for filter/sort test
            tag.mapping = {'artist': 'artist'}
            self.files.append(audio_path)
            self.audio_tags.append(tag)
    
    def tearDown(self):
        self.tmpdir.cleanup()
    
    def _create_model_and_table(self, tags=None):
        """Create a TagModel and TagTable with test data."""
        if tags is None:
            tags = self.audio_tags
        
        headerdata = [
            ('Filename', '__filename'),
            ('Artist', 'artist'),
            ('Title', 'title'),
            ('Album', 'album'),
            ('Track', 'track'),
            ('Year', 'year'),
        ]
        
        model = TagModel(headerdata, tags)
        table = TagTable()
        table.setModel(model)
        table.show()
        QApplication.processEvents()
        
        return model, table
    
    def _select_row(self, table, row):
        """Select a specific row in the table."""
        model = table.model()
        index = model.index(row, 0)
        table.selectionModel().select(
            index, 
            table.selectionModel().SelectionFlag.Select | table.selectionModel().SelectionFlag.Rows
        )
        QApplication.processEvents()
    
    def _get_selected_file(self, table):
        """Get the filepath of the currently selected file."""
        selected_rows = table.selectedRows
        if not selected_rows:
            return None
        return table.model().taginfo[selected_rows[0]].filepath
    
    def test_selection_preserved_after_filter(self):
        """Test that selection is correctly preserved after applying a filter."""
        model, table = self._create_model_and_table()
        
        # Select the first row (Artist 0)
        self._select_row(table, 0)
        selected_file = self._get_selected_file(table)
        self.assertEqual(selected_file, self.files[0])
        
        # Apply a filter that matches Artist 0
        table.applyFilter('Artist 0')
        QApplication.processEvents()
        
        # After filter, the selected row should still be Artist 0
        # The row number might change but the file should be the same
        selected_file_after = self._get_selected_file(table)
        self.assertEqual(
            selected_file_after, self.files[0],
            "Selection should point to the same file after filtering"
        )
        
        # Clear filter
        table.applyFilter('')
        QApplication.processEvents()
        
        # Selection should still be valid
        selected_file_cleared = self._get_selected_file(table)
        self.assertEqual(
            selected_file_cleared, self.files[0],
            "Selection should point to the same file after clearing filter"
        )
    
    def test_selection_preserved_after_sort(self):
        """Test that selection is correctly preserved after sorting."""
        model, table = self._create_model_and_table()
        
        # We need an artist that will actually move. 
        # Artist 0 is at index 0. If we sort descending by artist, 
        # Artist 4 will be at 0, and Artist 0 will be at index 4.
        # Let's select Artist 0.
        self._select_row(table, 0)
        selected_file = self._get_selected_file(table)
        self.assertEqual(selected_file, self.files[0])
        
        # Sort by Artist descending
        model.sortByFields(['artist'], reverse=True)
        QApplication.processEvents()
        
        # After sort, the selected file should still be 'Artist 0'
        selected_file_after = self._get_selected_file(table)
        self.assertEqual(
            selected_file_after, selected_file,
            "Selection should point to the same file after sorting"
        )
        
        # Verify the row actually changed
        self.assertNotEqual(table.selectedRows[0], 0, "Row position should have changed after sort")
    
    def test_selection_preserved_after_reload_selected(self):
        """Test that selection is preserved after reloadSelected."""
        model, table = self._create_model_and_table()
        
        # Select the second file (Artist 1)
        self._select_row(table, 1)
        selected_file = self._get_selected_file(table)
        self.assertEqual(selected_file, self.files[1])
        
        # We can't easily test reloadSelected without real file I/O,
        # but we can test the restoreSelection mechanism directly
        # by simulating what happens during reload
        
        # Save selection
        saved = table.saveSelection()
        self.assertIn(self.files[1], saved)
        
        # Modify model (simulate reload by replacing taginfo)
        with model.reset_context():
            model.taginfo = self.audio_tags.copy()
        
        # Restore selection
        table.restoreSelection(saved)
        QApplication.processEvents()
        
        selected_file_after = self._get_selected_file(table)
        self.assertEqual(
            selected_file_after, self.files[1],
            "Selection should be restored correctly after reload"
        )
    
    def test_editing_after_filter_targets_correct_file(self):
        """Test that editing a cell after filtering targets the correct underlying file."""
        model, table = self._create_model_and_table()
        
        # Select Artist 0
        self._select_row(table, 0)
        self.assertEqual(model.taginfo[0].get('artist')[0], 'TestArtist0')
    
        # Apply filter to show only TestArtist0
        table.applyFilter('artist is "TestArtist0"')
        QApplication.processEvents()
    
        # Verify only one row is visible
        self.assertEqual(model.rowCount(), 1)
        self.assertEqual(model.taginfo[0].get('artist')[0], 'TestArtist0')
        
        # Get the index of the visible row
        index = model.index(0, 1)  # Artist column
        
        # Mock the underlying tag's get and mapping if necessary
        # But here we just want to see if setData calls setRowData correctly
        
        # We need to ensure newvalue != currentfile.get(tag, "") for it to call setRowData
        # currentfile.get('artist') returns ['TestArtist0']
        # newvalue will be 'ModifiedArtist'
        
        # Mock setRowData to avoid write() errors and just return success
        with patch.object(model, 'setRowData', return_value=('TestArtist0', {'artist': 'ModifiedArtist'})) as mock_set:
            new_value = 'ModifiedArtist'
            # We must use the model's setData
            result = model.setData(index, new_value, Qt.ItemDataRole.EditRole)
            self.assertTrue(result, "setData should return True when setRowData is called")
            
            # Verify the correct row index was passed to setRowData
            mock_set.assert_called_once()
            args, _ = mock_set.call_args
            self.assertEqual(args[0], 0)  # Row 0
            self.assertEqual(args[1], {'artist': ['ModifiedArtist']})
    
    def test_editing_after_sort_targets_correct_file(self):
        """Test that editing a cell after sorting targets the correct underlying file."""
        model, table = self._create_model_and_table()
    
        # Sort by Artist descending (TestArtist4 first)
        model.sortByFields(['artist'], reverse=True)
        QApplication.processEvents()
    
        # Row 0 should now be TestArtist4 (originally at index 4)
        self.assertEqual(model.taginfo[0].get('artist')[0], 'TestArtist4')
        
        index = model.index(0, 1)  # Artist column
    
        # Use a new value different from current
        new_value = 'ModifiedAfterSort'
        self.assertNotEqual(model.taginfo[0].get('artist')[0], new_value)

        # Mock setRowData
        with patch.object(model, 'setRowData', return_value=('TestArtist4', {'artist': 'ModifiedAfterSort'})) as mock_set:
            result = model.setData(index, new_value, Qt.ItemDataRole.EditRole)
            self.assertTrue(result, "setData should return True when setRowData is called")
            
            # Verify row 0 was edited
            mock_set.assert_called_once()
            args, _ = mock_set.call_args
            self.assertEqual(args[0], 0)
            self.assertEqual(args[1], {'artist': ['ModifiedAfterSort']})
    
    def test_selection_after_folder_change(self):
        """Test that selection mapping works correctly after folder change."""
        model, table = self._create_model_and_table()
        
        # Select first file
        self._select_row(table, 0)
        selected_file = self._get_selected_file(table)
        self.assertEqual(selected_file, self.files[0])
        
        # Get the original dirpath
        original_dir = self.audio_tags[0].dirpath
        
        # Change folder in the model
        model.changeFolder(original_dir, '/new/folder/path')
        QApplication.processEvents()
        
        # The taginfo should still have the same objects, just with updated dirpath
        selected_file_after = self._get_selected_file(table)
        self.assertEqual(
            selected_file_after, self.files[0],
            "Selection should remain valid after folder change"
        )
        
        # Verify the dirpath was updated
        self.assertEqual(
            model.taginfo[0].dirpath, '/new/folder/path',
            "Dirpath should be updated after folder change"
        )
    
    def test_multiple_selection_preserved(self):
        """Test that multiple row selection is preserved."""
        model, table = self._create_model_and_table()
        
        # Select multiple rows (0 and 2)
        model_index = model.index
        selection = table.selectionModel()
        
        for row in [0, 2]:
            index = model_index(row, 0)
            selection.select(index, selection.SelectionFlag.Select | selection.SelectionFlag.Rows)
        
        QApplication.processEvents()
        
        selected_files = [self.files[i] for i in table.selectedRows]
        self.assertEqual(len(selected_files), 2)
        self.assertIn(self.files[0], selected_files)
        self.assertIn(self.files[2], selected_files)
        
        # Apply filter that matches both
        table.applyFilter('Artist')
        QApplication.processEvents()
        
        # Both should still be selected
        selected_files_after = [model.taginfo[i].filepath for i in table.selectedRows]
        self.assertEqual(len(selected_files_after), 2)
        self.assertIn(self.files[0], selected_files_after)
        self.assertIn(self.files[2], selected_files_after)
    
    def test_selection_after_clear_and_reload(self):
        """Test selection handling when clearing all and reloading."""
        model, table = self._create_model_and_table()
        
        # Select TestArtist1 (which should be at index 1 initially)
        self.assertEqual(model.taginfo[1].get('artist')[0], 'TestArtist1')
        selected_file = self.files[1]

        self._select_row(table, 1)
        self.assertEqual(self._get_selected_file(table), selected_file)
        
        # Clear all
        table.clearAll()
        QApplication.processEvents()
        self.assertEqual(model.rowCount(), 0)
        
        # To avoid unpredictable reordering by unique(), 
        # let's mock it to return the list as is.
        # We must use the absolute path for patching
        with patch('puddlestuff.puddleobjects.unique', side_effect=lambda x: x):
            # Reload with same data
            table.fillTable(self.audio_tags, append=False)
            QApplication.processEvents()
        
        # Selection should be restored (by filepath)
        selected_file_after = self._get_selected_file(table)
        self.assertEqual(
            selected_file_after, selected_file,
            "Selection should be restored after clear and reload"
        )


class TestSelectionWithRealFiles(unittest.TestCase):
    """Test selection safety using real audio files."""
    
    @classmethod
    def setUpClass(cls):
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            cls.ffmpeg_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            cls.ffmpeg_available = False
        
        cls.app = QApplication.instance() or QApplication([])
    
    def setUp(self):
        if not self.ffmpeg_available:
            self.skipTest("ffmpeg not available")
        
        self.tmpdir = tempfile.TemporaryDirectory()
        
        # Create real audio files
        self.files = []
        for i, (ext, codec_args) in enumerate(TEST_FORMATS):
            audio_path = create_test_audio_file(self.tmpdir.name, ext, codec_args)
            self.files.append(audio_path)
    
    def tearDown(self):
        self.tmpdir.cleanup()
    
    def _create_model_and_table(self, files=None):
        if files is None:
            files = self.files
        
        tags = []
        for i, f in enumerate(files):
            tag = Tag(f)
            if tag:
                # Add distinctive metadata with simple names for filtering
                tag['artist'] = f'TestArtist{i}'
                tag['title'] = f'TestTitle{i}'
                tag['album'] = f'TestAlbum{i}'
                tag.save()
                tags.append(tag)
        
        headerdata = [
            ('Filename', '__filename'),
            ('Artist', 'artist'),
            ('Title', 'title'),
            ('Album', 'album'),
        ]
        
        model = TagModel(headerdata, tags)
        table = TagTable()
        table.setModel(model)
        table.show()
        QApplication.processEvents()
        
        return model, table
    
    def _select_row(self, table, row):
        model = table.model()
        index = model.index(row, 0)
        table.selectionModel().select(
            index, 
            table.selectionModel().SelectionFlag.Select | table.selectionModel().SelectionFlag.Rows
        )
        QApplication.processEvents()
    
    def _get_selected_file(self, table):
        selected_rows = table.selectedRows
        if not selected_rows:
            return None
        return table.model().taginfo[selected_rows[0]].filepath
    
    def test_real_files_selection_after_filter(self):
        """Test selection with real audio files after filtering."""
        model, table = self._create_model_and_table()
        
        if model.rowCount() < 2:
            self.skipTest("Need at least 2 files")
        
        # Select first row
        self._select_row(table, 0)
        selected_file = self._get_selected_file(table)
        
        # Get the artist of the selected file
        artist = model.taginfo[0].get('artist')
        
        # Filter by that artist using the correct syntax
        table.applyFilter(f'artist="{artist}"')
        QApplication.processEvents()
        
        # Selected file should still be the same
        selected_file_after = self._get_selected_file(table)
        self.assertEqual(
            selected_file_after, selected_file,
            "Selection should point to same file after filtering real files"
        )
    
    def test_real_files_selection_after_sort(self):
        """Test selection with real audio files after sorting."""
        model, table = self._create_model_and_table()
        
        if model.rowCount() < 2:
            self.skipTest("Need at least 2 files")
        
        # Select row 1
        self._select_row(table, 1)
        selected_file = self._get_selected_file(table)
        
        # Sort by artist
        model.sortByFields(['artist'], reverse=False)
        QApplication.processEvents()
        
        # Selected file should still be the same
        selected_file_after = self._get_selected_file(table)
        self.assertEqual(
            selected_file_after, selected_file,
            "Selection should point to same file after sorting real files"
        )


if __name__ == '__main__':
    unittest.main()