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
- [ ] **Expanded Format Support**: Add support for missing formats found in Mp3tag (DSD, AIFF, Matroska/WebM, OptimFROG, TAK, TTA).
- [ ] **Enhanced Export Templates**: Implement user-defined templates for generating collection reports in HTML, RTF, and CSV formats.
- [ ] **Asynchronous Lookups**: Add the ability to cancel active tag source lookups (Amazon, Discogs, MusicBrainz) without freezing the UI.
- [ ] **Advanced Artwork Management**: Provide granular control over artwork saving (Tag only, File only, Both, or None).
- [ ] **Massive Code Cleanup**: Refactor legacy code to improve performance and maintainability.
- [ ] **Enhanced Duplicate Finder**: A robust tool to find and manage duplicate tracks based on metadata and audio fingerprints.

### Linux Ecosystem Integration
- [ ] **Native Playlist Management**: Automatic playlist creation and management while editing, integrated with Linux media players.
- [ ] **Expanded Library Support**: Implement native support for Rhythmbox and MPD libraries.
- [ ] **CLI Modernization**: Improve the console version to support full scripting and automated batch processing.
- [ ] **Wayland Optimization**: Ensure seamless performance and UI scaling on Wayland-based desktops, but maintaining support for 11.
- [ ] **Theme Awareness**: Better integration with system-wide Dark Mode and custom GTK/Qt themes.

### Distribution & Documentation
- [ ] **Universal Packages**: Official support for Flatpak and AppImage to reach more users across different distributions.
- [ ] **Comprehensive Plugin API Docs**: Detailed documentation to encourage community-driven plugin development.

### Statistics & Analytics
- [ ] **Library Statistics**: Provide meaningful insights into your music collection (genre distribution, bitrate analysis, missing metadata reports).
