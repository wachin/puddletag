"""Routines and script to back up audio metadata (puddletag
audioinfo.Tag objects).

Data is stored as json."""

import json
import logging
import os
import sys
from optparse import OptionParser

from ... import audioinfo
from ...audioinfo import tag_to_json

logger = logging.getLogger(__name__)


def tags_to_json(dirpath, fields=None):
    ret = []
    for fn in os.listdir(dirpath):
        fn = os.path.join(dirpath, fn)
        if os.path.isdir(fn):
            ret.extend(tags_to_json(fn, fields))
            continue
        tag = tag_to_json(fn, fields)
        if tag:
            ret.append(tag)
    return ret


def backup_dir(dirpath, fn, fields=None):
    with open(fn, "w") as fo:
        fo.write(json.dumps(tags_to_json(dirpath, fields)))


def main():
    usage = "Usage: %prog [-f FIELDS] [-b dirpath | -r] filename"
    parser = OptionParser(usage=usage)

    parser.add_option(
        "-b",
        "--backup",
        dest="backup",
        default="",
        help="Backs up all audio tags in dirpath to filename.",
        metavar="BACKUP",
    )
    parser.add_option(
        "-r",
        "--restore",
        dest="restore",
        default="",
        help="Restores audio tags found in filename.",
        metavar="RESTORE",
        action="store_true",
    )
    parser.add_option(
        "-f",
        "--fields",
        dest="fields",
        default="",
        help="Comma separated list of fields. "
        "Backed up data will be restricted to this list, but if "
        "restored will overwrite the complete file.",
        metavar="FIELDS",
        action="store",
    )

    options, filenames = parser.parse_args()
    if not (options.backup or options.restore):
        parser.print_help()
        sys.exit()

    if not filenames:
        logger.error("Fatal Error: Require filename to write backup to!")
        sys.exit(1)

    filename = filenames[0]

    if os.path.exists(filename) and options.backup:
        logger.error(f"Fatal Error: Backup file, {filename} already exists")
        sys.exit(2)

    fields = options.fields if options.fields else None
    if fields:
        fields = [z.strip() for z in fields.split(",")]

    if options.backup:
        backup_dir(options.backup, filename, fields)
    elif options.restore:
        restore_backup(filename)


def restore_backup(fn):
    with open(fn) as f:
        tags = json.loads(f.read())
    for tag in tags:
        try:
            path = tag["__path"]
        except KeyError:
            logger.error("A file was backed up without a file path")
            continue
        try:
            audio = audioinfo.Tag(path)
        except Exception:
            logger.exception("Couldn't restore %s", path)
            continue

        if "__image" in tag:
            del tag["__image"]

        audio.clear()
        audio.update(tag)
        audio.save()


if __name__ == "__main__":
    main()
