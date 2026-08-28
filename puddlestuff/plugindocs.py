"""Helpers for documenting bundled plugins."""

import os
from dataclasses import dataclass

BUILTIN_PLUGIN_DIR = os.path.join(os.path.dirname(__file__), "plugins")


@dataclass(frozen=True)
class PluginDoc:
    name: str
    module: str
    version: str
    author: str
    description: str


def _rst_text(text):
    return text.replace("\\", "\\\\").replace("*", r"\*")


def iter_plugin_docs(plugins=None):
    """Yield plugin metadata from the bundled plugin registry."""
    if plugins is None:
        from .pluginloader import get_plugins

        plugins = get_plugins(BUILTIN_PLUGIN_DIR)

    for plugin in plugins:
        yield PluginDoc(
            name=str(plugin.get("name", "")),
            module=str(plugin.get("module", "")),
            version=str(plugin.get("version", "")),
            author=str(plugin.get("author", "")),
            description=str(plugin.get("description", "")),
        )


def plugins_rst(plugins=None):
    """Return reStructuredText documenting bundled plugins."""
    rows = sorted(
        iter_plugin_docs(plugins),
        key=lambda row: row.name.lower(),
    )

    lines = [
        ".. _generated_plugin_reference:",
        "",
        "Generated Plugin Reference",
        "--------------------------",
        "",
        "This table is generated from the bundled plugin registry shown in the Plugins dialog.",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "",
        "   * - Plugin",
        "     - Module",
        "     - Version",
        "     - Author",
        "     - Description",
    ]

    for row in rows:
        lines.extend(
            [
                f"   * - {_rst_text(row.name)}",
                f"     - ``{row.module}``",
                f"     - {_rst_text(row.version)}",
                f"     - {_rst_text(row.author)}",
                f"     - {_rst_text(row.description)}",
            ]
        )

    return "\n".join(lines) + "\n"
