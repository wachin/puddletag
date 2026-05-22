# PuddleTag Roadmap

Our goal is to make PuddleTag the premier audio metadata editor for the Linux community, rivaling and exceeding the features of established tools like Mp3tag while remaining deeply integrated into the Linux ecosystem.

## Accomplished Tasks
- [x] **Spanish Language Support**: Fixed naming collisions that prevented Spanish (es_ES) translations from being packaged in Debian and other distributions.
- [x] **Improved Locale Detection**: Updated language matching to support both `es_ES` and `es-ES` formats, ensuring better compatibility with system settings.
- [x] **Packaging Refactor**: Restructured the translation modules to follow standard Python package conventions, resolving installation issues.
- [x] **Distribution Fixes**: Updated `setup.py` and `MANIFEST.in` to ensure all translation files and data assets are correctly included in build artifacts.
- [x] **PyQt6 Migration**: Updated the codebase to use the modern PyQt6 framework for better performance and future-proofing.

## Planned Features & Improvements

### Core Functionality
- [x] **Full Unicode Support**: Ensure the user interface and tagging engine remain fully Unicode compliant for global metadata compatibility.
- [x] **Expanded Format Support**: Added support for AIFF, WAV, AAC, DSF (DSD), OptimFROG, TAK, and TTA (TrueAudio).
- [ ] **Missing Formats**: Implement support for remaining formats like Matroska/WebM (pending Mutagen updates).
- [x] **Enhanced Export Templates**: Implemented user-defined templates for generating collection reports in HTML, RTF, and CSV formats with loop support.
- [x] **Asynchronous Lookups**: Added the ability to cancel active tag source lookups (Amazon, Discogs, MusicBrainz) and submissions.
- [x] **Advanced Artwork Management**: Added granular control over artwork saving (Tag only, File only, Both, or None) in Tag Settings.
- [ ] **Massive Code Cleanup**: Refactor legacy code to improve performance and maintainability.
- [ ] **Enhanced Duplicate Finder**: A robust tool to find and manage duplicate tracks based on metadata and audio fingerprints.

### Linux Ecosystem Integration
- [x] **Native Playlist Management**: Automatic playlist creation and management while editing, with a new "Update playlist automatically on save" option.
- [ ] **Expanded Library Support**: Implement native support for Rhythmbox and MPD libraries.
- [x] **CLI Modernization**: Transitioned to `argparse` and added dedicated CLI commands for exporting and tagging without the GUI.
- [x] **Wayland Optimization**: Improved support for Wayland-based desktops by ensuring proper platform detection while maintaining X11 fallback.
- [x] **Theme Awareness**: Added support for Dark Mode, accessible through the General Settings.

### Distribution & Documentation
- [ ] **Automated Documentation**: Ensure new features are automatically added to the help files in `/docs` and `/docsrc`.
- [ ] **Universal Packages**: Official support for Flatpak and AppImage to reach more users across different distributions.
- [ ] **Comprehensive Plugin API Docs**: Detailed documentation to encourage community-driven plugin development.

### Statistics & Analytics
- [ ] **Library Statistics**: Provide meaningful insights into your music collection (genre distribution, bitrate analysis, missing metadata reports).
