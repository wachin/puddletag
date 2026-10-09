# PuddleTag Roadmap

Our goal is to make PuddleTag the premier audio metadata editor for the Linux community, rivaling and exceeding the features of established tools like Mp3tag while remaining deeply integrated into the Linux ecosystem.

## Accomplished Tasks
- [x] **Spanish Language Support**: Fixed naming collisions that prevented Spanish (es_ES) translations from being packaged.
- [x] **Improved Locale Detection**: Support for both `es_ES` and `es-ES` formats.
- [x] **Spanish Locale Fallback**: Spanish UI translations now fall back from regional locales such as `es_EC` to the available `es_ES` catalog.
- [x] **Packaging & Distribution**: Restructured translation modules and updated `setup.py`/`MANIFEST.in`.
- [x] **PyQt6 Migration**: Modernized the UI framework for better performance.
- [x] **Expanded Format Support**: Added AIFF, WAV, AAC, DSF (DSD), OptimFROG, TAK, and TTA (TrueAudio).
- [x] **Enhanced Export Templates**: Template-based export for HTML, RTF, and CSV with loop support.
- [x] **Asynchronous Lookups**: Ability to cancel active tag source lookups and submissions.
- [x] **Advanced Artwork Management**: Granular control over artwork saving (Tag, File, Both, None).
- [x] **Native Playlist Management**: Automatic playlist updates on save.
- [x] **Expanded Library Support**: Added native support for Rhythmbox and **MPD** (Music Player Daemon).
- [x] **CLI Modernization**: Transitioned to `argparse` with dedicated commands (headless mode).
- [x] **Wayland Optimization**: Improved platform detection and HiDPI scaling.
- [x] **Theme Awareness**: Added a dedicated **Dark Mode**.
- [x] **Integrated Logging**: Centralized logging with a built-in viewer in the Help menu.
- [x] **Library Statistics**: Detailed insights into genre, format, and bitrate distribution.
- [x] **Enhanced Duplicate Finder**: A robust tool to find and manage duplicates across the library.
- [x] **Automated Format Documentation**: Supported format help text is generated from the live audio format registry.
- [x] **Automated Function Documentation**: Action function reference docs are generated from the live action function registry.
- [x] **Automated Tag Source & Plugin Documentation**: Tag source and bundled plugin reference tables are generated from their live registries.
- [x] **Comprehensive Plugin API Docs**: Detailed plugin API reference for community developers covering module attributes, action functions, tag sources, dockable dialogs, music libraries, and helper APIs.
- [x] **Plugin Loader Fix**: User plugins in `~/.puddletag/plugins` load again; the `puddlestuff.plugins.` import prefix introduced for issue #41 had made them unloadable.
- [x] **Undefined Name Bug Fixes**: First code-cleanup pass fixed five runtime NameError bugs in live code found by pyflakes (id3, amg, musicbrainz, rhythmbox and the id3_tools plugin).
- [x] **Code Modernization (Ruff)**: Fixed 644/644 lint errors; all 95 files formatted; zero lint errors remaining.
- [x] **Export Error Handling**: Fixed error swallowing in export dialog and export_tags plugin; added proper exception handling and logging.
- [x] **Backup/Restore Image Handling**: Fixed image restoration in `export_tags` plugin and `tagbackup.py` using `b64_to_img()`.
- [x] **Real Audio Round-Trip Test Infrastructure**: Created automated tests for 7 audio formats (FLAC, OGG, OPUS, MP3, M4A, WAV, AIFF) using ffmpeg-generated fixtures; covers format round-trip, artwork preservation, multi-value fields, Unicode tags, and tag deletion.

## Planned Features & Improvements

### Data Safety & Core Functionality (Phase 1-2)
- [ ] **Selection/Model Safety**: Audit and add regression tests for selection staleness after filter/sort/reload/folder change (P2)
- [ ] **Preview Mode & Undo/Redo**: Add tests for preview editing, undo/redo, cancel, commit, selection changes (P3)
- [ ] **Format Function Test Suite**: Comprehensive tests for 106 format-string functions (P2)
- [ ] **Converter Edge Cases**: Test filename↔tag converters with spaces, Unicode, special chars (P2)
- [ ] **WMA Format Testing**: Verify read/write capability for WMA format (P2)
- [ ] **Tag Source Verification**: Verify Amazon, AMG tag source status; document or remove (P2)

### Format Reliability (Phase 3)
- [ ] **Missing Formats**: Implement support for remaining formats like Matroska/WebM (pending Mutagen updates).
- [ ] **Test All Supported Formats**: Complete read/write verification for all 20+ supported formats.
- [ ] **Identify Read-Only Formats**: Document formats with limited write support.

### Actions/Functions (Phase 4)
- [ ] **Action Function Testing**: Test all 74 actions for correctness.
- [ ] **Format-String Parser Test Suite**: Edge cases for empty args, Unicode, nested functions.

### Usability (Phase 5)
- [ ] **Artwork Management Reliability**: Extended tests for artwork preservation across all operations.
- [ ] **Tag Source UI Responsiveness**: Audit QThread usage; add timeouts.
- [ ] **CLI Edge Cases**: Test CLI with Unicode paths, spaces, special characters.

### Distribution & Documentation
- [ ] **Massive Code Cleanup**: Refactor legacy code to improve performance and maintainability. First pass done (undefined-name bugs in live code fixed); remaining pyflakes warnings are in dead code (demo `__main__` blocks, `mainwin/teststuff.py`, the unloadable `export_tags` plugin), plus unused-import and unused-variable sweeps still to do.
- [ ] **AppImage Package**: Official support for AppImage. Build script (`create_appimage.sh`) and AppStream metainfo (`puddletag.appdata.xml`) are in place; a first build is pending testing (requires `python3-pyinstaller` and the auto-downloaded `appimagetool`).
- [ ] **Create TESTING.md**: Document test procedures, fixture strategy, and manual verification steps.

### Disabled (available for fork developers)
- [ ] **Flatpak Package**: Official support for Flatpak. Disabled because the maintainer no longer uses Flatpak and cannot test it. Developers who fork this repository are welcome to pick this up.
