import struct

import mutagen.id3
from mutagen.id3 import ParseID3v1

from . import apev2, id3

APEv2_Tag = apev2.Tag

_v2_nums = {2, 3, 4}

ID3_V1 = "id3_v1"
ID3_V2 = "id3_v2"
APEv2 = "ape_v2"

TAG_TYPES = [ID3_V1, ID3_V2, APEv2]


def apev2_values(fn):
    assert isinstance(fn, str)

    return APEv2_Tag(fn).usertags


def convert_id3_frames(frames):
    mapping = id3.Tag.mapping
    return {mapping.get(k, k): v.get_value() for k, v in id3.handle(frames)}


def fullread(fileobj, size):
    data = fileobj.read(size)
    if len(data) != size:
        raise EOFError
    return data


def has_apev2(fn):
    if isinstance(fn, str):
        with open(fn, "rb") as fileobj:
            return _has_apev2(fileobj)
    return _has_apev2(fn)


def _has_apev2(fileobj):
    try:
        fileobj.seek(-160, 2)
    except OSError:
        return False

    footer = fileobj.read()
    return b"APETAGEX" in footer


def has_v1(fn):
    if isinstance(fn, str):
        with open(fn, "rb") as fileobj:
            return _has_v1(fileobj)
    return _has_v1(fn)


def _has_v1(fileobj):
    try:
        fileobj.seek(-128, 2)
        return "TAG" == struct.unpack("3s", fullread(fileobj, 3))[0]
    except (OSError, struct.error, EOFError):
        return False


def get_v2(fn):
    if isinstance(fn, str):
        with open(fn, "rb") as fileobj:
            return _get_v2(fileobj)
    return _get_v2(fn)


def _get_v2(fileobj):
    size = 5
    try:
        id3, vmaj, vrev = struct.unpack(">3sBB", fullread(fileobj, size))
    except EOFError:
        return

    if id3 == "ID3" and vmaj in _v2_nums:
        return (2, vmaj, vrev) if vrev != 0 else (2, vmaj)
    return


def id3v1_values(fn):
    if isinstance(fn, str):
        with open(fn, "rb") as fileobj:
            fileobj.seek(-128, 2)
            frames = ParseID3v1(fileobj.read(128))
    else:
        fileobj = fn
        fileobj.seek(-128, 2)
        frames = ParseID3v1(fileobj.read(128))
    if frames:
        return convert_id3_frames(frames)


def id3v2_values(fn):
    assert isinstance(fn, str)

    try:
        frames = mutagen.id3.ID3(fn)
    except Exception:  # noqa: BLE001
        return None
    if frames:
        return convert_id3_frames(frames)


def id3_tags(fn):
    if isinstance(fn, str):
        with open(fn, "rb") as fileobj:
            return _id3_tags(fileobj)
    return _id3_tags(fn)


def _id3_tags(fileobj):
    version = []

    try:
        version = [(1, 1)] if has_v1(fileobj) else []
    except EOFError:
        return []

    fileobj.seek(0)
    v2 = get_v2(fileobj)
    if v2:
        version.append(v2)
    return version


def tags_in_file(fn, to_check=(ID3_V1, ID3_V2, APEv2)):
    if isinstance(fn, str):
        with open(fn, "rb") as fileobj:
            return _tags_in_file(fileobj, fn, to_check)
    return _tags_in_file(fn, fn, to_check)


def _tags_in_file(fileobj, fn, to_check):
    if ID3_V1 in to_check and ID3_V2 in to_check:
        tags = ["ID3v" + ".".join(map(str, z)) for z in id3_tags(fileobj)]
    elif ID3_V1 in to_check:
        tags = ["ID3v1.1"] if has_v1(fileobj) else []
    elif ID3_V2 in to_check:
        tags = get_v2(fileobj)
        tags = ["ID3v" + ".".join(map(str, tags))] if tags else []
    else:
        tags = []

    if APEv2 in to_check and has_apev2(fn):
        tags.append("APEv2")
    return tags

    if ID3_V1 in to_check and ID3_V2 in to_check:
        tags = ["ID3v" + ".".join(map(str, z)) for z in id3_tags(fileobj)]
    elif ID3_V1 in to_check:
        tags = ["ID3v1.1"] if has_v1(fileobj) else []
    elif ID3_V2 in to_check:
        tags = get_v2(fileobj)
        tags = ["ID3v" + ".".join(map(str, tags))] if tags else []
    else:
        tags = []

    if APEv2 in to_check and has_apev2(fn):
        tags.append("APEv2")
    return tags


_value_types = {
    APEv2: apev2_values,
    ID3_V1: id3v1_values,
    ID3_V2: id3v2_values,
}


def tag_values(fn, tag):
    tag = tag.lower()
    if tag.startswith("id3v1"):
        tag = ID3_V1
    elif tag.startswith("id3v2"):
        tag = ID3_V2
    elif tag.startswith("ape"):
        tag = APEv2

    if tag not in TAG_TYPES:
        return {}

    return _value_types[tag](fn)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    # f = open(filename, 'rb')
    print(tags_in_file(filename))
    print(id3v1_values(filename))
    print(id3v2_values(filename))
    print(apev2_values(filename))
