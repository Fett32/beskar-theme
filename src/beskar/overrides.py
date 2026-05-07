"""Load user theme overrides from ~/.config/beskar/theme.toml."""

import tomllib
from pathlib import Path
from PySide6.QtGui import QColor

from beskar.tokens import key_map

_THEME_FILE = Path.home() / ".config" / "beskar" / "theme.toml"

# Derived from the canonical token registry.
_KEY_MAP = key_map()


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
