# puddletag

![Version](https://img.shields.io/badge/version-2.6.0-blue.svg)
![License](https://img.shields.io/badge/license-GPLv3-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![PyPI](https://img.shields.io/pypi/v/puddletag.svg)
![Linting](https://img.shields.io/badge/linting-ruff-261230.svg)
![Ruff Status](https://img.shields.io/badge/ruff-0%20errors-brightgreen.svg)
![Tests](https://img.shields.io/badge/tests-28%20passed-brightgreen.svg)
![Qt](https://img.shields.io/badge/GUI-PyQt6-green.svg)

![Screenshot](docs/_images/5.png)

puddletag is an audio tag editor (primarily created) for GNU/Linux similar to the
Windows program, Mp3tag. Unlike most taggers for GNU/Linux, it uses a
**spreadsheet-like layout** so that all the tags you want to edit by hand are visible
and easily editable.

The usual tag editor features are supported like extracting tag information from
filenames, renaming files based on their tags by using patterns and basic tag editing.

Then there're _Functions_, which can do things like replace text, trim it, do case
conversions, etc. _Actions_ can automate repetitive tasks. Doing web lookups using
AcoustID, Amazon, Discogs (does cover art too!), FreeDB and MusicBrainz is also
supported.

[Documentation](https://docs.puddletag.net/) ·
[Changelog](changelog) ·
[Issue Tracker](https://github.com/puddletag/puddletag/issues) ·
[Contributing](#-contributing)

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

## 🚀 Getting Started

There are two ways to run puddletag from source: using **system packages**
(recommended on Debian, Ubuntu and derivatives), or using a **Python virtual
environment** with pip (works on any distribution).

### Option 1: System packages (Debian, Ubuntu and derivatives)

Install all the dependencies as system packages:

```sh
sudo apt install python3 python3-pyqt6 python3-pyqt6.qtsvg python3-mutagen \
    python3-configobj python3-pyparsing python3-unidecode python3-lxml \
    python3-acoustid libchromaprint-tools
```

> **Note:** `python3-lxml` is required by the Discogs/HTML tag-source parsers, and
> `python3-acoustid` + `libchromaprint-tools` provide AcoustID (fingerprint
> recognition) support. Both are optional at runtime but recommended for the full
> feature set.

> **Optional extras:**
> - `python3-levenshtein` — enables the Jaro/Jaro-Winkler duplicate-finding
>   algorithms (without it, puddletag falls back to difflib's SequenceMatcher).
> - `python3-pytest` — only needed to run the test suite during development.

Then clone the repository and run puddletag:

```sh
git clone https://github.com/puddletag/puddletag.git
cd puddletag
python3 puddletag
```

No virtual environment, no pip — everything runs with your system's Python.

### Option 2: Virtual environment (venv + pip)

Use this method if your distribution doesn't package all the dependencies, or if
you prefer isolated environments. You only need `python3` and `python3-venv`
(on Debian/Ubuntu: `sudo apt install python3-venv`).

```sh
git clone https://github.com/puddletag/puddletag.git
cd puddletag
python3 -m venv .
bin/pip3 install -r requirements.txt
bin/python3 puddletag
```

This keeps all dependencies inside the repository's `venv` directory without
touching your system Python.

## 📦 Installing from a package

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

## 🧰 Dependencies

| Dependency | Purpose | Debian/Ubuntu package |
|---|---|---|
| [Python 3](https://www.python.org/) | Runtime | `python3` |
| [PyQt6](https://pypi.org/project/PyQt6/) | GUI framework | `python3-pyqt6` |
| Qt6 SVG | SVG icon rendering | `python3-pyqt6.qtsvg` |
| [Mutagen](https://pypi.org/project/mutagen/) | Audio tagging library | `python3-mutagen` |
| [pyparsing](https://pypi.org/project/pyparsing/) | Pattern parsing | `python3-pyparsing` |
| [configobj](https://pypi.org/project/configobj/) | Configuration files | `python3-configobj` |
| [unidecode](https://pypi.org/project/Unidecode/) | Unicode transliteration | `python3-unidecode` |
| [lxml](https://pypi.org/project/lxml/) | HTML tag-source parsing | `python3-lxml` |
| [pyacoustid](https://pypi.org/project/pyacoustid/) | AcoustID lookups | `python3-acoustid` |
| [Chromaprint](http://acoustid.org/chromaprint) | Audio fingerprinting (`fpcalc`) | `libchromaprint-tools` |
| [Levenshtein](https://pypi.org/project/Levenshtein/) *(optional)* | Jaro/Jaro-Winkler dupe search | `python3-levenshtein` |

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

See
[Puddletag Modernization Log to 2026 Standards.md](Puddletag%20Modernization%20Log%20to%202026%20Standards.md)
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

For translation testing and editing, see
[TRANSLATION_TESTING.md](TRANSLATION_TESTING.md).

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
