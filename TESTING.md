# Puddletag Testing Guide

This document describes the testing infrastructure, procedures, and manual verification steps for Puddletag.

## Test Suite Overview

### Automated Tests (pytest)

**Location**: `tests/`

**Run all tests**:
```bash
QT_QPA_PLATFORM=offscreen python3 -m pytest tests/ -v
```

**Run specific test module**:
```bash
QT_QPA_PLATFORM=offscreen python3 -m pytest tests/test_audio_roundtrip.py -v
```

**Test Categories**:
| Test File | Description | Dependencies |
|-----------|-------------|--------------|
| `test_audio_roundtrip.py` | Real audio format read/write round-trips | ffmpeg, mutagen |
| `test_cli.py` | Command-line interface tests | None |
| `test_export.py` | Export template processing | None |
| `test_field_translations.py` | Translation catalog verification | None |
| `test_formats.py` | Audio format registry documentation | None |
| `test_functiondocs.py` | Action function documentation | None |
| `test_playlist.py` | M3U playlist auto-update | None |
| `test_plugindocs.py` | Plugin documentation generation | None |
| `test_pluginloader.py` | Plugin loading mechanism | None |
| `test_statistics.py` | Statistics calculation | None |
| `test_tagsourcedocs.py` | Tag source documentation | None |
| `test_translations.py` | Translation system | None |

### Linting (ruff)

**Check code style**:
```bash
ruff check puddlestuff/
```

**Auto-fix issues**:
```bash
ruff check puddlestuff/ --fix
```

**Format code**:
```bash
ruff format puddlestuff/
```

## Audio Round-Trip Test Infrastructure

### Fixture Strategy

The audio round-trip tests (`test_audio_roundtrip.py`) create real audio files on-the-fly using **ffmpeg** rather than relying on pre-bundled fixtures. This ensures:

1. **No copyrighted content** — generated silence contains no licensed audio
2. **Deterministic** — same test file created every run
3. **Format coverage** — tests 7 formats: FLAC, OGG, OPUS, MP3, M4A, WAV, AIFF
4. **Isolation** — each test runs in a temporary directory

### Test Coverage

The `TestAudioRoundTrip` class covers:

| Test Method | Formats | Description |
|-------------|---------|-------------|
| `test_format_roundtrip` | All 7 | Write tags → save → reload → verify all fields |
| `test_artwork_preservation` | FLAC, MP3, OGG | Add artwork → edit unrelated tag → verify artwork persists |
| `test_multivalue_fields` | All 7 | Write multi-value artist → verify list preserved |
| `test_unicode_tags` | All 7 | Write Unicode tags (Cyrillic, Japanese, Spanish) |
| `test_tag_deletion` | All 7 | Write tag → delete → verify removed/empty |
| `test_readonly_fields_preserved` | All 7 | Verify length/bitrate not corrupted by tag edits |

### Adding New Format Tests

To add a new format to `TEST_FORMATS`:

1. Add entry to `TEST_FORMATS` list in `test_audio_roundtrip.py`:
```python
('ext', ['-c:a', 'codec'], True),  # ext=extension, codec=ffmpeg encoder
```

2. Ensure ffmpeg supports the codec (`ffmpeg -encoders | grep codec`)

3. Run the test to verify:
```bash
QT_QPA_PLATFORM=offscreen python3 -m pytest tests/test_audio_roundtrip.py::TestAudioRoundTrip::test_format_roundtrip -v
```

### Known Limitations

- **M4A artwork**: Currently fails to preserve artwork in test environment (known mutagen/ffmpeg interaction issue)
- **WMA**: Not tested — requires `ffmpeg -c:a wmav2` which may not be available in all distributions
- **DSF/DFF/APE/WV/MPC/OFR/TAK/TTA**: No ffmpeg encoder readily available for test file generation

## Manual GUI Verification

Since some functionality requires a running GUI, manual verification is needed for:

### Selection & Model Safety
1. **Filter test**: Load directory → apply filter → select file → verify correct file edited
2. **Sort test**: Load directory → sort by column → select file → verify correct file edited
3. **Reload test**: Load directory → select file → reload → verify selection preserved
4. **Folder change test**: Load directory → change folder → verify selection maps correctly

### Preview Mode & Undo/Redo
1. **Enable preview**: Ctrl+Shift+P → edit tags → verify preview highlighting
2. **Undo in preview**: Make changes → Ctrl+Z → verify preview changes undone
3. **Redo in preview**: Undo → Ctrl+Shift+Z → verify preview changes redone
4. **Cancel preview**: Make changes → Disable preview mode → confirm discard → verify no changes saved
5. **Commit preview**: Make changes → Write Previews (Ctrl+W) → verify changes saved
6. **Selection change in preview**: Enable preview → edit file A → select file B → verify preview updates
7. **Switch files with preview**: Enable preview → edit file A → select file B → re-select file A → verify preview preserved

### Artwork Management
1. **Add artwork**: Drag image to artwork panel → save → reload → verify artwork present
2. **Edit tags with artwork**: Add artwork → edit year/genre → save → reload → verify artwork intact
3. **Remove artwork**: Clear artwork → save → reload → verify artwork removed
4. **Multiple artwork**: Add multiple images → save → reload → verify all present

### Export Functionality
1. **CSV export**: Select files → Export → CSV → verify columns and quoting
2. **HTML export**: Select files → Export → HTML → open in browser → verify table structure
3. **RTF export**: Select files → Export → RTF → open in editor → verify formatting
4. **Custom template**: Create template with `$loop()` → export → verify iteration
5. **Error handling**: Export to read-only location → verify error dialog shown

### Tag Sources (Network)
1. **MusicBrainz search**: Open tag source dialog → search → verify results populate
2. **Cancel search**: Start search → cancel → verify no freeze
3. **Apply results**: Select match → apply → verify tags populated

### CLI Commands
```bash
# Test basic commands
python3 puddletag --help
python3 puddletag tag --help
python3 puddletag export --help

# Test with actual files (use temp directory)
python3 puddletag tag -f "%artist% - %title%" /path/to/test/files
python3 puddletag export -t csv /path/to/test/files -o /tmp/export.csv
```

## Development Environment Setup

### Required System Packages (Debian/Ubuntu)
```bash
sudo apt install python3-pytest python3-ffmpeg ffmpeg python3-mutagen \
    python3-pyqt6 python3-unidecode
```

### Python Dependencies
```bash
pip install pytest hypothesis qtpy
# Or use system packages:
sudo apt install python3-pytest python3-hypothesis
```

### Running the Application for Manual Testing
```bash
QT_QPA_PLATFORM=offscreen python3 puddletag
# Or for GUI (requires display):
python3 puddletag
```

## Continuous Integration

The test suite is designed to run in headless environments (CI/CD) using `QT_QPA_PLATFORM=offscreen`.

### GitHub Actions Example
```yaml
- name: Run tests
  run: |
    QT_QPA_PLATFORM=offscreen python3 -m pytest tests/ -v
    ruff check puddlestuff/
```

## Test Development Guidelines

1. **Never modify user's music library** — always use temporary directories
2. **Use generated fixtures** — create test files programmatically with ffmpeg/mutagen
3. **Test behavior, not implementation** — assert on observable outcomes
4. **Separate network tests** — tag source tests should be marked as integration tests
5. **Document manual verification** — for GUI-only features, provide step-by-step procedures
6. **Keep tests fast** — unit tests should complete in <1s each; integration tests <10s

## Debugging Test Failures

### Verbose Output
```bash
QT_QPA_PLATFORM=offscreen python3 -m pytest tests/test_audio_roundtrip.py -v -s
```

### Single Test with Debug
```bash
QT_QPA_PLATFORM=offscreen python3 -c "
import tempfile, os, subprocess
from tests.test_audio_roundtrip import create_test_audio_file
with tempfile.TemporaryDirectory() as tmpdir:
    f = create_test_audio_file(tmpdir, 'flac', ['-c:a', 'flac'])
    print(f'Created: {f}')
"
```

### Lint Failures
```bash
ruff check puddlestuff/ --show-source
ruff format --check puddlestuff/ --diff
```

## Version Compatibility

Tested with:
- Python 3.11+
- PyQt6 6.9+
- Mutagen 1.47+
- ffmpeg 6.0+
- pytest 8.0+
- hypothesis 6.100+

## Troubleshooting

### "ffmpeg not found"
Install ffmpeg: `sudo apt install ffmpeg`

### "mutagen not found"
Install mutagen: `sudo apt install python3-mutagen` or `pip install mutagen`

### "QT_QPA_PLATFORM=offscreen" not working
Ensure `libqt6gui6` and `qt6-gtk-platformtheme` are installed.

### Tests hang on import
Mock problematic modules (see `test_playlist.py` for pattern):
```python
sys.modules['puddlestuff.mainwin.funcs'] = MagicMock()
```

## Summary of Verified Functionality (as of 2026-10-08)

| Feature | Automated Test | Manual Verification | Status |
|---------|----------------|---------------------|--------|
| Audio format round-trip (7 formats) | ✅ | — | Verified |
| Artwork preservation (FLAC, MP3, OGG) | ✅ | — | Verified |
| Multi-value fields | ✅ | — | Verified |
| Unicode tags | ✅ | — | Verified |
| Tag deletion | ✅ | — | Verified |
| M3U playlist auto-update | ✅ | — | Verified |
| Export template processing | ✅ | — | Verified |
| Export error handling | ✅ | — | Verified |
| Backup/restore image handling | ✅ | — | Verified |
| Selection after filter/sort | ❌ | Required | Pending |
| Preview mode undo/redo | ❌ | Required | Pending |
| Tag source network operations | ❌ | Required | Pending |
| CLI edge cases | ❌ | Required | Pending |

✅ = Automated test exists and passes  
❌ = Requires manual verification or test not yet implemented