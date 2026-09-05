import os
import pickle
import traceback

import mutagen
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog

from ...puddletag import add_shortcuts
from .. import status

last_fn = {"fn": "~"}


def save_tags(files, fn):
    tags = []
    for f in files:
        try:
            tags.append(mutagen.File(f))
        except Exception:  # noqa: BLE001
            traceback.print_exc()
    with open(fn, "wb") as output:
        pickle.dump(tags, output)


def export_tags():
    selectedFile = QFileDialog.getSaveFileName(None, "Save tags", last_fn["fn"], "*.*")
    fn = selectedFile[0]
    if fn:
        save_tags((f.filepath for f in status["selectedfiles"]), fn)
        last_fn["fn"] = os.path.dirname(fn)


def init(parent=None):
    def sep():
        k = QAction(parent)
        k.setSeparator(True)
        return k

    action = QAction("Export tags", parent)
    action.triggered.connect(export_tags)
    add_shortcuts("&Plugins", [sep(), action, sep()])
