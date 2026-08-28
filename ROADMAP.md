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

## Planned Features & Improvements

## Development Notes
- Debian 12 package reference lists are available in `packages_available_debian12_pyqt6.txt` and `packages_available_debian12_python3.txt` for checking installable Python/PyQt6 dependencies during development.
- Debian packages currently used during development include `python3-sphinx`, `python3-sphinx-bootstrap-theme`, `python3-unidecode`, `python3-pytest`, and `linguist-qt6`.
- Stop development when a new Debian repository package is required. Record the package name and wait for the developer to install it before continuing.

### Core Functionality
- [ ] **Missing Formats**: Implement support for remaining formats like Matroska/WebM (pending Mutagen updates).
- [ ] **Massive Code Cleanup**: Refactor legacy code to improve performance and maintainability. First pass done (undefined-name bugs in live code fixed); remaining pyflakes warnings are in dead code (demo `__main__` blocks, `mainwin/teststuff.py`, the unloadable `export_tags` plugin), plus unused-import and unused-variable sweeps still to do.

### Distribution & Documentation
- [ ] **AppImage Package**: Official support for AppImage. Build script (`create_appimage.sh`) and AppStream metainfo (`puddletag.appdata.xml`) are in place; a first build is pending testing (requires `python3-pyinstaller` and the auto-downloaded `appimagetool`).

### Disabled (available for fork developers)
- [ ] **Flatpak Package**: Official support for Flatpak. Disabled because the maintainer no longer uses Flatpak and cannot test it. Developers who fork this repository are welcome to pick this up.
