"""Helpers for documenting tag sources."""

from dataclasses import dataclass

from .constants import CHECKBOX, COMBO, SPINBOX, TAGLIST, TEXT

PREFERENCE_TYPES = {
    TEXT: "text",
    COMBO: "combo",
    CHECKBOX: "checkbox",
    TAGLIST: "tag list",
    SPINBOX: "spinbox",
}


@dataclass(frozen=True)
class TagSourceDoc:
    name: str
    group_by: tuple
    preferences: tuple
    supports_submit: bool


def _clean_label(label):
    return label.replace("&", "").strip()


def _rst_text(text):
    return text.replace("\\", "\\\\").replace("*", r"\*")


def _preference_text(preference):
    label = _clean_label(str(preference[0]))
    type_name = PREFERENCE_TYPES.get(preference[1], str(preference[1]))
    return f"{label} ({type_name})"


def iter_tag_source_docs(sources=None):
    """Yield tag source metadata from the registered tag sources."""
    if sources is None:
        from .tagsources import tagsources as sources

    for source in sources:
        try:
            instance = source()
        except Exception:
            continue

        group_by = tuple(
            str(field)
            for field in getattr(instance, "group_by", ()) or ()
            if field
        )
        preferences = tuple(
            _preference_text(preference)
            for preference in getattr(instance, "preferences", ()) or ()
            if preference
        )

        yield TagSourceDoc(
            name=str(getattr(instance, "name", source)),
            group_by=group_by,
            preferences=preferences,
            supports_submit=hasattr(instance, "submit"),
        )


def tag_sources_rst(sources=None):
    """Return reStructuredText documenting registered tag sources."""
    rows = sorted(
        iter_tag_source_docs(sources),
        key=lambda row: row.name.lower(),
    )

    lines = [
        ".. _generated_tag_source_reference:",
        "",
        "Generated Tag Source Reference",
        "------------------------------",
        "",
        "This table is generated from the tag source registry used by the Tag Sources window.",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "",
        "   * - Tag source",
        "     - Group by",
        "     - Preferences",
        "     - Submission",
    ]

    for row in rows:
        group_by = ", ".join(_rst_text(field) for field in row.group_by)
        group_by = group_by if group_by else "None"
        preferences = "; ".join(_rst_text(pref) for pref in row.preferences)
        preferences = preferences if preferences else "None"
        lines.extend([
            f"   * - {_rst_text(row.name)}",
            f"     - {group_by}",
            f"     - {preferences}",
            f"     - {'Yes' if row.supports_submit else 'No'}",
        ])

    return "\n".join(lines) + "\n"
