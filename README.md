<div align="center">

# puddletag

![Screenshot](docs/_images/5.png)

**A powerful, simple, audio tag editor for GNU/Linux**

puddletag is an audio tag editor similar to the Windows program
[Mp3tag](https://www.mp3tag.de/en/). Unlike most taggers for GNU/Linux, it uses a
**spreadsheet-like layout** so that all the tags you want to edit by hand are visible
and easily editable.

[Report a Bug](https://github.com/puddletag/puddletag/issues) ·
[Request a Feature](https://github.com/puddletag/puddletag/issues) ·
[Documentation](https://docs.puddletag.net/) ·
[Changelog](changelog)

</div>

---

## Badges

| | |
|---|---|
| **Version** | [![Version](https://img.shields.io/badge/version-2.6.0-blue.svg)](changelog) |
| **License** | [![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0.html) |
| **Python** | [![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/) |
| **PyPI** | [![PyPI](https://img.shields.io/pypi/v/puddletag.svg)](https://pypi.org/project/puddletag/) |
| **Linting** | [![Code Style: ruff](https://img.shields.io/badge/linting-ruff-261230.svg)](https://github.com/astral-sh/ruff) |
| **Lint Status** | ![Errors](https://img.shields.io/badge/ruff-0%20errors-brightgreen.svg) |
| **Tests** | [![Tests](https://img.shields.io/badge/tests-28%20passed-brightgreen.svg)](tests/) |
| **Qt Toolkit** | [![Qt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://www.riverbankcomputing.com/software/pyqt/) |

---

## ✨ Features

- **Spreadsheet-like layout** — all your tags visible and editable at once
- **Extract tag info from filenames** — using patterns
- **Rename files based on tags** — using patterns
- **Functions** — replace text, trim it, case conversions, and much more
- **Actions** — automate repetitive tasks
- **Web lookups** — AcoustID, Amazon, Discogs, FreeDB, MusicBrainz
- **Music library integration** — Quod Libet, Rhythmbox, MPD
- **Dark Mode** — accessible in General Settings
- **CLI mode** — headless export and tagging (argparse subcommands)
- **Built-in log viewer** — in the Help menu

## 🎵 Supported Formats

**ID3v1** and **ID3v2** (mp3, wav, aac, aiff, dsf) · **MP4** (mp4, m4a, etc.) ·
**VorbisComments** (ogg, flac) · **Musepack** (mpc) · **Monkey's Audio** (.ape) ·
**WavPack** (wv) · **OptimFROG** (ofr, ofs) · **TAK** (tak) · **TrueAudio** (tta) ·
**WMA** (wma) · **Opus** (opus)

## 📦 Installation

### PyPI

Puddletag is available on [PyPI](https://pypi.org/project/puddletag/).

In addition to the full releases, every time we merge a PR or commit a change, we
automatically release a new version on
[TestPyPI](https://test.pypi.org/project/puddletag/), so if you want to try a brand
new feature or a recent bugfix, you can give these pre-releases a try.

There are several tools to install puddletag via PyPI, for example
[pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-to-the-user-site),
[pipx](https://pypa.github.io/pipx/installation/),
[pipenv](https://pipenv.pypa.io/en/latest/), and several others. Choose the one that
suits best your workflow, but we strongly recommend you create an isolated, local
environment when installing third-party software.

### Distributions package

<details>
<summary><b>Debian</b></summary>

```
apt install puddletag
```

Contact: @sandrotosi
</details>

<details>
<summary><b>Ubuntu</b></summary>

```
apt install puddletag
```

Contact: @sandrotosi
</details>

<details>
<summary><b>Gentoo</b></summary>

1. overlay: https://github.com/istitov/stuff/
2. add overlay: `sudo layman -a stuff`
3. install: `sudo emerge -av puddletag`

Contact: @DolphinStKom
</details>

<details>
<summary><b>Arch Linux</b></summary>

puddletag is currently part of the [AUR](https://aur.archlinux.org/packages/puddletag/):

```sh
git clone https://aur.archlinux.org/puddletag.git
cd puddletag
makepkg -si
```

</details>

<details>
<summary><b>Fedora</b></summary>

Available since Fedora 32.

```
dnf install puddletag
```

</details>

<details>
<summary><b>Nix / NixOS</b></summary>

Available for channels 24.05 and unstable

On NixOS:

```sh
nix-env -iA nixos.puddletag
```

On non-NixOS:

```sh
# without flakes:
nix-env -iA nixpkgs.puddletag
# with flakes:
nix profile install nixpkgs#puddletag
```

NixOS configuration — add the following Nix code to your NixOS Configuration, usually
located in `/etc/nixos/configuration.nix`:

```nix
environment.systemPackages = [
  pkgs.puddletag
];
```

</details>

<details>
<summary><b>Brew / macOS</b></summary>

_Support needed — open an issue if you are interested in working on it_
</details>

### From Source

If you seek the bleeding edge of puddletag, or want to contribute (we welcome all
contributions!), you can install and/or run via source code.

First, install the dependencies. This step differs per distribution; on **Debian/Ubuntu**
you can run:

```sh
apt install python3 python3-mutagen python3-configobj python3-pyparsing \
            python3-pyqt6 python3-pyqt6.qtsvg python3-unidecode
```

For documentation and tests during development on Debian, also install:

```sh
apt install python3-sphinx python3-sphinx-bootstrap-theme python3-pytest
```

For translation testing and editing, see
[TRANSLATION_TESTING.md](TRANSLATION_TESTING.md).

Then, clone the repo and run puddletag:

```sh
git clone https://github.com/puddletag/puddletag
cd puddletag
./puddletag
```

Alternatively, you can use a
[virtual environment](https://docs.python.org/3/library/venv.html) to install the
dependencies, which only requires python and pip:

```sh
git clone https://github.com/puddletag/puddletag.git
cd puddletag
python3 -m venv .
bin/pip3 install -r requirements.txt
bin/python3 puddletag
```

## 🧰 Dependencies

| Dependency | Purpose |
|---|---|
| [Python 3](https://www.python.org/) | Runtime |
| [PyQt6](https://pypi.org/project/PyQt6/) | GUI framework |
| [Mutagen](https://pypi.org/project/mutagen/) | Audio tagging library |
| [pyparsing](https://pypi.org/project/pyparsing/) | Pattern parsing |
| [configobj](https://pypi.org/project/configobj/) | Configuration files |
| [unidecode](https://pypi.org/project/Unidecode/) | Unicode transliteration |
| [Chromaprint](http://acoustid.org/chromaprint) *(recommended)* | AcoustID support |

## 🧪 Development

### Running the tests

```sh
python3 -m pytest tests/
```

### Linting

The codebase is kept at **zero ruff errors** and fully formatted:

```sh
ruff check puddlestuff/
ruff format --check puddlestuff/
```

See [Puddletag Modernization Log to 2026 Standards.md](Puddletag%20Modernization%20Log%20to%202026%20Standards.md)
for the full modernization history.

### Recent development highlights

This repository has recently received renewed maintenance work, including:

- **PyQt6 migration** and Wayland/HiDPI startup improvements
- **Complete 2026 code modernization** — 644 ruff errors fixed, 95 files formatted,
  28/28 tests passing
- **Spanish translation packaging fixes** — locale fallback from regional Spanish
  locales such as `es_EC` to the available `es_ES` catalog
- **Expanded audio format support** — WAV, AAC, AIFF, DSF, OptimFROG, TAK, TTA
- **Template-based export** — HTML, RTF, and CSV with loop support
- **Native playlist save/update support**
- **Music library integration** — Rhythmbox and MPD
- **Dark mode**, built-in log viewer, library statistics, duplicate-finder improvements
- **CLI commands** for export and tag editing
- **AppImage packaging** — `create_appimage.sh` build script and AppStream metainfo
- **Comprehensive plugin API reference** for plugin developers, and a fix so user
  plugins in `~/.puddletag/plugins` load again

## 🤝 Contributing

We welcome all contributions! To get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure your code passes the linting and test suite before submitting:

```sh
ruff check puddlestuff/ && ruff format --check puddlestuff/ && python3 -m pytest tests/
```

## 📄 License

`puddletag` is licensed under the **GPLv3**, which you can find in its entirety at
[http://www.gnu.org/licenses/gpl-3.0.html](http://www.gnu.org/licenses/gpl-3.0.html).

## 🙏 Credits

puddletag is maintained by its
[community of contributors](https://github.com/puddletag/puddletag/graphs/contributors).

Originally created by concentricpuddle.
