import logging
import os

from . import findfunc
from .audioinfo import Tag

logger = logging.getLogger(__name__)


def cli_export(paths, template_name, output_file):

    # Load tags from paths
    tags = []
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for f in files:
                    try:
                        t = Tag(os.path.join(root, f))
                        if t:
                            tags.append(t)
                    except Exception:
                        logger.exception("Failed to load %s", os.path.join(root, f))
        else:
            try:
                t = Tag(path)
                if t:
                    tags.append(t)
            except Exception:
                logger.exception("Failed to load %s", path)

    if not tags:
        print("No audio files found.")
        return

    # Use ExportDialog's processing logic (even if it's a QDialog, we can use the method)
    # We need a dummy dialog or just extract the logic.
    # For now, I'll extract the logic to a static method or just duplicate it here.

    templates = {
        "CSV": "%artist%;%album%;%title%;%track%;%year%;%genre%",
        "HTML": """<html>
<head><title>Export</title></head>
<body>
<table border="1">
  <tr>
    <th>Artist</th>
    <th>Album</th>
    <th>Title</th>
  </tr>
$loop(%artist%)  <tr>
    <td>%artist%</td>
    <td>%album%</td>
    <td>%title%</td>
  </tr>
$loopend()</table>
</body>
</html>""",
        "RTF": "Artist: %artist%\\line Album: %album%\\line Title: %title%\\line\\line",
    }

    template = templates.get(template_name, templates["CSV"])

    # Simple loop processing (duplicated from export.py for now)
    import re

    loop_match = re.search(r"\$loop\((.*?)\)(.*?)\$loopend\(\)", template, re.DOTALL)
    if loop_match:
        sort_field = loop_match.group(1).strip("%")
        loop_body = loop_match.group(2)
        sorted_tracks = sorted(tags, key=lambda t: t.get(sort_field, ""))
        loop_result = ""
        for track in sorted_tracks:
            loop_result += findfunc.parsefunc(loop_body, track)
        result = (
            template[: loop_match.start()] + loop_result + template[loop_match.end() :]
        )
    else:
        result = ""
        for track in tags:
            result += findfunc.parsefunc(template, track) + "\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"Exported {len(tags)} tracks to {output_file}")


def cli_tag(paths, tags_to_set):
    count = 0
    for path in paths:
        try:
            t = Tag(path)
            if t:
                for k, v in tags_to_set.items():
                    if v is not None:
                        t[k] = v
                t.save()
                count += 1
        except Exception as e:  # noqa: BLE001
            print(f"Error tagging {path}: {e}")

    print(f"Updated {count} files.")
