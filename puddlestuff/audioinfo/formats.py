"""Helpers for documenting supported audio formats."""


def _extension_list(extensions):
    if isinstance(extensions, str):
        return [extensions]
    return list(extensions or [])


def _module_filetypes(module):
    if hasattr(module, "filetype"):
        yield module.filetype
    yield from getattr(module, "filetypes", ())


def _audio_format_name(mutagen_type, tag_type, tag_format, extensions):
    name = getattr(tag_type, "filetype", None)
    if name is not None:
        return name

    try:
        return tag_type().filetype
    except AttributeError:
        mutagen_name = getattr(mutagen_type, "__name__", str(mutagen_type))
        if mutagen_name == "ASF":
            return "WMA/ASF"
        if mutagen_name.endswith("FileType"):
            if extensions == ["mp3"]:
                return "MP3"
            return tag_format
        return mutagen_name


def iter_supported_formats(tag_modules=None):
    """Yield supported formats from registered audioinfo modules.

    Each yielded item is ``(tag_format, audio_format, extensions)`` where
    ``extensions`` is a sorted tuple without leading dots.
    """
    if tag_modules is None:
        from . import tag_modules

    rows = {}
    for module in tag_modules:
        for filetype in _module_filetypes(module):
            if len(filetype) < 4:
                continue

            mutagen_type, tag_type, tag_format, extensions = filetype[:4]
            extension_list = _extension_list(extensions)
            key = (
                str(tag_format),
                str(
                    _audio_format_name(
                        mutagen_type, tag_type, tag_format, extension_list
                    )
                ),
            )
            rows.setdefault(key, set()).update(extension_list)

    for (tag_format, audio_format), extensions in rows.items():
        yield tag_format, audio_format, tuple(sorted(extensions))


def supported_formats_summary(tag_modules=None):
    """Return a compact human-readable supported formats summary."""
    rows = sorted(
        iter_supported_formats(tag_modules),
        key=lambda row: (row[0].lower(), row[1].lower(), row[2]),
    )
    parts = []
    for tag_format, audio_format, extensions in rows:
        ext_text = ", ".join(extensions)
        parts.append(f"{audio_format} ({tag_format}: {ext_text})")
    return "Supported formats: " + "; ".join(parts) + "."


def supported_formats_rst(tag_modules=None):
    """Return reStructuredText documenting supported formats."""
    return supported_formats_summary(tag_modules) + "\n"
