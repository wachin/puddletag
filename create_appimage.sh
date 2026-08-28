#!/bin/bash
# Build an AppImage for puddletag.
#
# Requirements:
#   - python3 with the project dependencies installed (see README)
#   - PyInstaller: 'apt install python3-pyinstaller' (or 'pip install pyinstaller')
#   - appimagetool: downloaded automatically to ./tools if not found in PATH
#
# Notes:
#   - fpcalc (chromaprint) is not bundled. AcoustID support requires it to be
#     installed on the target system.
#   - If FUSE is unavailable, appimagetool is retried with
#     --appimage-extract-and-run.
#
# Usage: ./create_appimage.sh

set -e

cd "$(dirname "$0")"

APPDIR=puddletag.AppDir
TOOLS_DIR=tools
ARCH=${ARCH:-$(uname -m)}

version=$(python3 -c "from puddlestuff import version_string; print(version_string)")
output="puddletag-${version}-${ARCH}.AppImage"

if ! command -v pyinstaller >/dev/null; then
    echo "pyinstaller not found. Install it with: apt install python3-pyinstaller"
    exit 1
fi

echo "Building puddletag with PyInstaller"
pyinstaller --noconfirm --clean --onedir --name puddletag \
    --collect-submodules puddlestuff.plugins \
    --collect-submodules puddlestuff.tagsources \
    --collect-submodules puddlestuff.libraries \
    --collect-data puddlestuff \
    puddletag

echo "Assembling ${APPDIR}"
rm -rf "${APPDIR}"
mkdir -p "${APPDIR}/usr/bin" \
         "${APPDIR}/usr/share/applications" \
         "${APPDIR}/usr/share/metainfo" \
         "${APPDIR}/usr/share/icons/hicolor/256x256/apps"

cp -r dist/puddletag/. "${APPDIR}/usr/bin/"

# TryExec breaks desktop-file validation inside an AppImage.
grep -v '^TryExec=' puddletag.desktop > "${APPDIR}/puddletag.desktop"
cp "${APPDIR}/puddletag.desktop" "${APPDIR}/usr/share/applications/"
cp puddletag.appdata.xml "${APPDIR}/usr/share/metainfo/puddletag.appdata.xml"
cp puddletag.png "${APPDIR}/puddletag.png"
cp puddletag.png "${APPDIR}/usr/share/icons/hicolor/256x256/apps/puddletag.png"

cat > "${APPDIR}/AppRun" <<'APPRUN'
#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/usr/bin/puddletag" "$@"
APPRUN
chmod +x "${APPDIR}/AppRun"

if command -v desktop-file-validate >/dev/null; then
    desktop-file-validate "${APPDIR}/puddletag.desktop"
fi

appimagetool=$(command -v appimagetool || true)
if [ -z "${appimagetool}" ]; then
    mkdir -p "${TOOLS_DIR}"
    appimagetool="${TOOLS_DIR}/appimagetool"
    if [ ! -x "${appimagetool}" ]; then
        echo "Downloading appimagetool"
        wget -q "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-${ARCH}.AppImage" \
            -O "${appimagetool}"
        chmod +x "${appimagetool}"
    fi
fi

echo "Creating ${output}"
if ! ARCH="${ARCH}" "${appimagetool}" "${APPDIR}" "${output}"; then
    echo "Retrying with --appimage-extract-and-run (needed when FUSE is unavailable)"
    ARCH="${ARCH}" "${appimagetool}" --appimage-extract-and-run "${APPDIR}" "${output}"
fi

echo "Done: ${output}"
