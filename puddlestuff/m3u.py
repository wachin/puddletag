import csv
import os
from os.path import abspath, dirname, normcase, normpath, splitdrive
from os.path import join as path_join

from PyQt6.QtWidgets import QFileDialog

from . import audioinfo
from .audioinfo.util import encode_fn
from .findfunc import tagtofilename


def commonpath(a, b):
    """Returns the longest common to 'paths' path.

    Unlike the strange commonprefix:
    - this returns valid path
    - accepts only two arguments
    """
    a = normpath(normcase(a))
    b = normpath(normcase(b))

    if a == b:
        return a

    while len(a) > 0:
        if a == b:
            return a

        if len(a) > len(b):
            a = dirname(a)
        else:
            b = dirname(b)

    return None


def relpath(target, base_path=os.curdir):
    """\
    Return a relative path to the target from either the current directory
    or an optional base directory.

    Base can be a directory specified either as absolute or relative
    to current directory."""
    # http://code.activestate.com/recipes/302594/

    base_path = normcase(abspath(normpath(base_path)))
    target = normcase(abspath(normpath(target)))

    if base_path == target:
        return "."

    # On the windows platform the target may be on a different drive.
    if splitdrive(base_path)[0] != splitdrive(target)[0]:
        return None

    common_path_len = len(commonpath(base_path, target))

    # If there's no common prefix decrease common_path_len should be less by 1
    base_drv, base_dir = splitdrive(base_path)
    if common_path_len == len(base_drv) + 1:
        common_path_len -= 1

    # if base_path is root directory - no directories up
    if base_dir == os.sep:
        dirs_up = 0
    else:
        dirs_up = base_path[common_path_len:].count(os.sep)

    ret = os.sep.join([os.pardir] * dirs_up)
    if len(target) > common_path_len:
        ret = path_join(ret, target[common_path_len + 1 :])

    return ret


def readm3u(path):
    # From http://forums.fedoraforum.org/showthread.php?p=1224109
    olddir = os.path.abspath(os.curdir)
    os.chdir(os.path.dirname(path))

    # List of mp3files
    mp3Files = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 1:
                # Skip blanks
                continue
            elif row[0].startswith("#"):
                # Ignore comments
                continue
            else:
                # store rule
                mp3Files.append(normpath(abspath(",".join(row))))

    os.chdir(olddir)
    return mp3Files


def exportm3u(tags, tofile, format=None, reldir=False, winsep=False):
    header = ["#EXTM3U"]

    if reldir:
        reldir = os.path.dirname(os.path.abspath(tofile))
        filenames = [relpath(f.filepath, reldir) for f in tags]
    else:
        filenames = [f.filepath for f in tags]

    if winsep:
        filenames = [f.replace("/", "\\") for f in filenames]

    if format is None:
        text = "\n".join(header + filenames)
    else:
        text = header
        extinfo = (
            f"#EXTINF: {int(f.length)}, {encode_fn(tagtofilename(format, f, False))}"
            for f in tags
        )
        [text.extend([z, y]) for z, y in zip(extinfo, filenames)]
        text = "\n".join(text)

    with open(tofile, "w") as playlist:
        playlist.write(text)


def auto_update_playlist(tags):
    """Automatically updates playlists in the directories of the given tags
    if the setting is enabled."""
    cparser = PuddleConfig()
    if not cparser.get("playlist", "auto_update", False):
        return

    # Group tags by directory
    dirs = defaultdict(list)
    for t in tags:
        dirs[os.path.dirname(t.filepath)].append(t)

    filepattern = cparser.get("playlist", "filepattern", "puddletag.m3u")
    extinfo = cparser.get("playlist", "extinfo", True)
    extpattern = cparser.get("playlist", "extpattern", "%artist% - %title%")
    reldir_setting = cparser.get("playlist", "reldir", False)
    winsep = cparser.get("playlist", "windows_separator", False)

    for d in dirs:
        # In Mp3tag, auto-playlist usually means a playlist for all files in that dir
        # We'll look for all tags in that directory from status['alltags']
        from .puddletag import status

        all_dir_tags = [
            t for t in status["alltags"] if os.path.dirname(t.filepath) == d
        ]

        if not all_dir_tags:
            continue

        # Use the first tag to generate the playlist filename if it has placeholders
        playlist_name = tagtofilename(filepattern, all_dir_tags[0])
        playlist_path = os.path.join(d, playlist_name)

        pattern = extpattern if extinfo else None
        exportm3u(all_dir_tags, playlist_path, pattern, reldir_setting, winsep)


from collections import defaultdict

from .puddleobjects import PuddleConfig

if __name__ == "__main__":
    filedlg = QFileDialog()
    filedlg.setFileMode(QFileDialog.FileMode.Directory)
    filedlg.setOption(QFileDialog.Option.ShowDirsOnly)
    filename = str(filedlg.getExistingDirectory(None, "Open Folder"))
    tags = []
    for z in os.listdir(filename):
        try:
            tag = audioinfo.Tag(os.path.join(filename, z))
            if tag:
                tags.append(tag)
        except Exception:  # noqa: BLE001, S110
            pass
    folder = str(filedlg.getSaveFileName(None, "Save File"))
    exportm3u(tags, folder)
