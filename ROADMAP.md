# PuddleTag Roadmap

Our goal is to make PuddleTag the premier audio metadata editor for the Linux community, rivaling and exceeding the features of established tools like Mp3tag while remaining deeply integrated into the Linux ecosystem.

## Accomplished Tasks
- [x] **Spanish Language Support**: Fixed naming collisions that prevented Spanish (es_ES) translations from being packaged.
- [x] **Improved Locale Detection**: Support for both `es_ES` and `es-ES` formats.
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

## Planned Features & Improvements

### Core Functionality
- [ ] **Missing Formats**: Implement support for remaining formats like Matroska/WebM (pending Mutagen updates).
- [ ] **Massive Code Cleanup**: Refactor legacy code to improve performance and maintainability.

### Distribution & Documentation
- [ ] **Automated Documentation**: Ensure new features are automatically added to the help files.
- [ ] **Universal Packages**: Official support for Flatpak and AppImage.
- [ ] **Comprehensive Plugin API Docs**: Detailed documentation for community developers.
