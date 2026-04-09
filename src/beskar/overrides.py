"""Load user theme overrides from ~/.config/beskar/theme.toml."""

import tomllib
from pathlib import Path
from PySide6.QtGui import QColor

_THEME_FILE = Path.home() / ".config" / "beskar" / "theme.toml"

# Maps theme.toml keys to beskar.colors attribute names
_KEY_MAP = {
    "surfaces": {
        "base": "SURFACE_BASE",
        "raised": "SURFACE_RAISED",
        "overlay": "SURFACE_OVERLAY",
        "input": "SURFACE_INPUT",
        "alt": "SURFACE_ALT",
    },
    "borders": {
        "default": "BORDER",
        "hover": "BORDER_HOVER",
    },
    "text": {
        "primary": "TEXT",
        "bright": "TEXT_BRIGHT",
        "slot": "TEXT_SLOT",
        "label": "TEXT_LABEL",
        "dim": "TEXT_DIM",
    },
    "accents": {
        "yellow": "ACCENT_YELLOW",
        "blue": "ACCENT_BLUE",
        "link": "ACCENT_LINK",
    },
    "semantic": {
        "highlight": "HIGHLIGHT",
        "selection_green": "SELECTION_GREEN",
        "terminal_green": "TERMINAL_GREEN",
        "button": "BUTTON",
        "button_text": "BUTTON_TEXT",
    },
}


def load_overrides() -> dict[str, QColor]:
    """Read theme.toml and return a dict of {attr_name: QColor}.

    Returns empty dict if file doesn't exist or can't be parsed.
    """
    if not _THEME_FILE.exists():
        return {}

    try:
        with open(_THEME_FILE, "rb") as f:
            data = tomllib.load(f)
    except Exception:
        return {}

    overrides = {}
    for section, keys in _KEY_MAP.items():
        section_data = data.get(section, {})
        for toml_key, attr_name in keys.items():
            value = section_data.get(toml_key)
            if value is not None:
                overrides[attr_name] = QColor(value)
    return overrides


def apply_overrides() -> None:
    """Load theme.toml and patch beskar.colors module globals."""
    import beskar.colors as colors_module
    for attr_name, color in load_overrides().items():
        setattr(colors_module, attr_name, color)
