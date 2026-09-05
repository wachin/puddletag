import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

status = {}


def connect_shortcut(action, enabled, disabled=None, togglecheck=None):
    controls = status["dialogs"]
    emits = defaultdict(list)

    for c in controls.values():
        [emits[sig].append(c) for sig in c.emits]

    if enabled in emits:
        [getattr(c, enabled).connect(action.setEnabled) for c in emits[enabled]]
    else:
        logger.error("No enable signal found for %s", action.text())
        action.setEnabled(False)

    if togglecheck and togglecheck in emits:
        [getattr(c, togglecheck).connect(action.setEnabled) for c in emits[togglecheck]]


def connect_control(control):
    controls = status["dialogs"]
    emits = defaultdict(list)

    for c in controls.values():
        [emits[sig].append(c) for sig in c.emits]

    for signal, slot in control.receives:
        if signal in emits:
            [getattr(c, signal).connect(slot) for c in emits[signal]]

    for c in controls.values():
        for signal, slot in c.receives:
            if signal in control.emits:
                getattr(control, signal).connect(slot)
