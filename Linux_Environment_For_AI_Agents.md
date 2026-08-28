# Complete Guide: Packages for AI Agents to Work on Linux (Debian 13)

Definitive guide to prepare a Linux environment where a code agent can investigate, analyze, compile, and document software projects.

## 1. Update Package Indices

```bash
sudo apt update
```

## 2. Main System Tools

These are the base tools that every agent needs:

```bash
sudo apt install -y \
  git \
  git-lfs \
  gh \
  python3 \
  python3-pip \
  python3-venv \
  python3-dev \
  build-essential \
  curl \
  wget \
  less
```

| Package | Command | Description |
|---------|---------|-------------|
| git | `git` | Version control, essential for working with repositories |
| git-lfs | `git lfs` | Git Large File Storage, for repositories with large files |
| gh | `gh` | GitHub CLI, to interact with GitHub directly from terminal |
| python3 | `python3` | Python interpreter, base for many tools |
| python3-pip | `pip3` | Python package manager |
| python3-venv | `python3 -m venv` | Python virtual environments |
| python3-dev | - | Python development files (headers) |
| build-essential | `gcc`, `make`, etc. | Essential compilers and build tools |
| curl | `curl` | HTTP client for APIs and downloads |
| wget | `wget` | File downloads |
| less | `less` | File viewer |

## 3. Code Search and Analysis

Tools for the agent to quickly search, analyze, and understand code:

```bash
sudo apt install -y \
  ripgrep \
  fd-find \
  jq \
  tree \
  bat \
  silversearcher-ag \
  ctags \
  universal-ctags
```

| Package | Command | Description |
|---------|---------|-------------|
| ripgrep | `rg` | Ultra-fast recursive search, respects `.gitignore` |
| fd-find | `fdfind` | File name search (faster than `find`) |
| jq | `jq` | JSON processor in command line |
| tree | `tree` | Directory structure visualization |
| bat | `bat` | Enhanced `cat` with syntax highlighting |
| silversearcher-ag | `ag` | Fast source code search |
| ctags / universal-ctags | `ctags` | Code index generation |

### Configure `fd` on Debian

On Debian, `fd-find` is installed as `fdfind`. To use `fd`:

```bash
mkdir -p ~/.local/bin
ln -sf "$(command -v fdfind)" ~/.local/bin/fd
```

## 4. Essential GNU Tools

The basic Unix toolset that every agent should know:

```bash
sudo apt install -y \
  findutils \
  coreutils \
  grep \
  sed \
  gawk \
  diffutils \
  xargs \
  parallel
```

| Package | Main Command | Description |
|---------|--------------|-------------|
| findutils | `find`, `xargs` | File search and processing |
| coreutils | `ls`, `cp`, `mv`, `cat`, `sort`, `uniq`, `wc`, etc. | Basic system tools |
| grep | `grep` | Pattern search in text |
| sed | `sed` | Command-line text editing |
| gawk | `awk` | Text and column processing |
| diffutils | `diff`, `comm` | File comparison |
| parallel | `parallel` | Parallel command execution |

## 5. Compression and Archives

To work with any file format:

```bash
sudo apt install -y \
  unzip \
  zip \
  tar \
  xz-utils \
  zstd \
  p7zip-full \
  rsync \
  file
```

| Package | Command | Description |
|---------|---------|-------------|
| unzip / zip | `unzip`, `zip` | ZIP format |
| tar | `tar` | tar/gz/bz2/xz archives |
| xz-utils | `xz`, `unxz` | XZ compression |
| zstd | `zstd`, `unzstd` | Zstandard compression (very fast) |
| p7zip-full | `7z` | Support for 7z and many formats |
| rsync | `rsync` | Efficient file synchronization |
| file | `file` | File type identification |

## 6. Executable Inspection Tools

To analyze binaries, libraries, and packages:

```bash
sudo apt install -y \
  binutils \
  elfutils \
  strace \
  ltrace \
  patchelf \
  objdump
```

| Package | Commands | Description |
|---------|----------|-------------|
| binutils | `readelf`, `objdump`, `strings`, `nm`, `strip`, `ar` | ELF binary analysis tools |
| elfutils | `eu-readelf`, `eu-objdump` | Alternative ELF utilities |
| strace | `strace` | System call tracing |
| ltrace | `ltrace` | Library call tracing |
| patchelf | `patchelf` | ELF modification (rpath, interpreter) |

### Usage Examples for the Agent:

```bash
# Identify a file
file program

# Analyze ELF dependencies
readelf -d program

# View binary sections
objdump -p program

# Extract readable strings
strings program

# View symbols
nm program

# Modify rpath
patchelf --set-rpath /my/path program
```

## 7. Debian Package Tools (.deb)

To investigate and create Debian packages:

```bash
sudo apt install -y \
  dpkg-dev \
  debhelper \
  devscripts \
  fakeroot \
  lintian \
  desktop-file-utils \
  dpkg-repack
```

| Package | Command | Description |
|---------|---------|-------------|
| dpkg-dev | `dpkg-deb`, `dpkg-buildpackage`, `dpkg-source` | Package development tools |
| debhelper | `dh` | Macros and helpers for Debian packaging |
| devscripts | `debuild`, `dch`, `debchange` | Scripts for Debian maintainers |
| fakeroot | `fakeroot` | Simulate root user for packaging |
| lintian | `lintian` | .deb package quality checker |
| desktop-file-utils | `desktop-file-validate` | .desktop file validation |
| dpkg-repack | `dpkg-repack` | Rebuild a .deb from an installed package |

## 8. AppImage Tools

To work with AppImage format:

```bash
sudo apt install -y \
  squashfs-tools \
  squashfuse \
  fuse3 \
  fuse
```

| Package | Command | Description |
|---------|---------|-------------|
| squashfs-tools | `unsquashfs`, `mksquashfs` | Extract/create squashfs filesystems |
| squashfuse | - | Mount squashfs without root |
| fuse3 / fuse | - | Filesystem in Userspace |

**Note:** Do not install `appimagetool` or `linuxdeploy` yet. First investigate what each project uses.

## 9. Network and Debugging Tools

For network debugging and HTTP requests:

```bash
sudo apt install -y \
  net-tools \
  iproute2 \
  socat \
  ncat \
  httpie \
  tmux \
  screen
```

| Package | Command | Description |
|---------|---------|-------------|
| net-tools | `netstat`, `ifconfig` | Classic network tools |
| iproute2 | `ip`, `ss` | Modern network tools |
| socat | `socat` | Bidirectional socket multiplexor |
| ncat | `ncat` | TCP/UDP client/server |
| httpie | `http` | More user-friendly HTTP client than curl |
| tmux | `tmux` | Terminal multiplexor |
| screen | `screen` | Terminal sessions |

## 10. Text and Documentation Tools

For generating and documenting:

```bash
sudo apt install -y \
  pandoc \
  texlive-base \
  groff \
  vim \
  nano \
  htop \
  btop
```

| Package | Command | Description |
|---------|---------|-------------|
| pandoc | `pandoc` | Universal document converter |
| texlive-base | `pdflatex` | LaTeX for PDF generation |
| groff | `groff` | Text formatting system |
| vim / nano | `vim`, `nano` | Text editors |
| htop / btop | `htop`, `btop` | Process monitoring |

## 11. Advanced Git Tools

For better version control:

```bash
sudo apt install -y \
  git \
  git-lfs \
  git-flow \
  gitk \
  tig
```

| Package | Command | Description |
|---------|---------|-------------|
| git-flow | `git flow` | Git workflow (feature, release, hotfix) |
| gitk | `gitk` | Graphical history viewer |
| tig | `tig` | Terminal git history viewer |

## 12. Code Analysis Tools

For static analysis and pattern detection:

```bash
sudo apt install -y \
  cppcheck \
  splint \
  nmcli
```

| Package | Command | Description |
|---------|---------|-------------|
| cppcheck | `cppcheck` | Static analysis for C/C++ |
| splint | `splint` | Static verifier for C |

## 13. Complete Installation Command (Copy and Paste)

To install all tools at once:

```bash
sudo apt update && sudo apt install -y \
   git \
   git-lfs \
   git-flow \
   gitk \
   tig \
   gh \
   python3 \
   python3-pip \
   python3-venv \
   python3-dev \
   build-essential \
   ripgrep \
   fd-find \
   jq \
   tree \
   bat \
   silversearcher-ag \
   universal-ctags \
   findutils \
   coreutils \
   grep \
   sed \
   gawk \
   diffutils \
   parallel \
   unzip \
   zip \
   tar \
   xz-utils \
   zstd \
   p7zip-full \
   rsync \
   file \
   binutils \
   elfutils \
   strace \
   ltrace \
   patchelf \
   dpkg-dev \
   debhelper \
   devscripts \
   fakeroot \
   lintian \
   desktop-file-utils \
   dpkg-repack \
   squashfs-tools \
   squashfuse \
   fuse3 \
   fuse \
   curl \
   wget \
   httpie \
   socat \
   ncat \
   net-tools \
   iproute2 \
   less \
   vim \
   nano \
   htop \
   btop \
   tmux \
   screen \
   pandoc \
   cppcheck
```

## 14. Post-Installation Configuration

### Configure `fd` on Debian

```bash
mkdir -p ~/.local/bin
ln -sf "$(command -v fdfind)" ~/.local/bin/fd
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Configure GitHub CLI

```bash
gh auth status
# If you haven't logged in:
gh auth login
```

### Configure Git with Your Proton Email

```bash
git config --global user.email "linuxfrontier@proton.me"
git config --global user.name "Your Name"
```

### Verify Everything with a Single Block

```bash
echo "=== Git ===" && git --version
echo "=== Git LFS ===" && git lfs version
echo "=== GitHub CLI ===" && gh --version | head -1
echo "=== Python ===" && python3 --version
echo "=== Pip ===" && pip3 --version
echo "=== Ripgrep ===" && rg --version | head -1
echo "=== fd ===" && fd --version
echo "=== jq ===" && jq --version
echo "=== Tree ===" && tree --version
echo "=== file ===" && file --version | head -1
echo "=== readelf ===" && readelf --version | head -1
echo "=== patchelf ===" && patchelf --version
echo "=== lintian ===" && lintian --version
echo "=== bat ===" && bat --version
echo "=== parallel ===" && parallel --version | head -1
echo "=== GitHub auth ===" && gh auth status 2>&1
```

## 15. What NOT to Install Yet?

For an agent that investigates code, do NOT install:

- PyQt6, PyInstaller, Nuitka (project dependencies)
- napari, Pyzo, CARA (specific applications)
- `pip install -r requirements.txt` (project dependencies)
- appimagetool, linuxdeploy (external binaries)

**First investigate what each project uses before installing its dependencies.**

## Summary of Categories

| Category | Packages | Purpose |
|----------|----------|---------|
| Git and GitHub | `git`, `git-lfs`, `git-flow`, `gh`, `tig` | Version control and GitHub |
| Python | `python3`, `pip3`, `python3-venv`, `python3-dev` | Python environment |
| Code search | `ripgrep`, `fd-find`, `bat`, `ag` | Find code quickly |
| Compilation | `build-essential`, `gcc`, `make`, `pkg-config` | Compile software |
| Binary analysis | `binutils`, `elfutils`, `strace`, `patchelf` | Analyze executables |
| Debian packages | `dpkg-dev`, `debhelper`, `lintian`, `fakeroot` | Create/verify .deb |
| AppImage | `squashfs-tools`, `squashfuse`, `fuse3` | Work with AppImage |
| Compression | `tar`, `zip`, `7z`, `zstd`, `xz` | Any format |
| Text and docs | `pandoc`, `vim`, `nano` | Edit and document |
| System | `htop`, `tmux`, `curl`, `wget` | Monitoring and network |

---

**Note:** This guide is designed so that a code agent can work autonomously on Linux, investigating repositories, analyzing code, inspecting binaries, and documenting findings without needing to install specific project dependencies.
