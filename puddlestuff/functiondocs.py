"""Helpers for documenting action functions."""

import csv
from dataclasses import dataclass


@dataclass(frozen=True)
class ActionFunctionDoc:
    key: str
    name: str
    preview: str
    arguments: tuple


def _parse_csv_line(line):
    return [
        item.strip()
        for item in next(csv.reader([line], skipinitialspace=True))
    ]


def _clean_label(label):
    return label.replace("&", "").strip()


def _rst_text(text):
    return text.replace("\\", "\\\\").replace("*", r"\*")


def iter_action_function_docs(function_map=None):
    """Yield action function metadata from the registered function map."""
    if function_map is None:
        from .functions import functions as function_map

    for key, function in sorted(function_map.items()):
        doc = getattr(function, "__doc__", None)
        if not doc:
            continue

        lines = [line.strip() for line in doc.splitlines() if line.strip()]
        if not lines:
            continue

        header = _parse_csv_line(lines[0])
        if len(header) < 2:
            continue

        arguments = []
        for line in lines[1:]:
            control = _parse_csv_line(line)
            if control:
                arguments.append(_clean_label(control[0]))

        yield ActionFunctionDoc(
            key=str(key),
            name=header[0],
            preview=header[1],
            arguments=tuple(arguments),
        )


def action_functions_rst(function_map=None):
    """Return reStructuredText documenting registered action functions."""
    rows = sorted(
        iter_action_function_docs(function_map),
        key=lambda row: row.name.lower(),
    )

    lines = [
        ".. _generated_function_reference:",
        "",
        "Generated Function Reference",
        "----------------------------",
        "",
        "This table is generated from the action function registry used by the Actions dialog.",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "",
        "   * - Function",
        "     - Registry key",
        "     - Preview text",
        "     - Arguments",
    ]

    for row in rows:
        arguments = "; ".join(_rst_text(arg) for arg in row.arguments)
        arguments = arguments if arguments else "None"
        lines.extend([
            f"   * - {_rst_text(row.name)}",
            f"     - ``{row.key}``",
            f"     - ``{row.preview}``",
            f"     - {arguments}",
        ])

    return "\n".join(lines) + "\n"
