"""Canonical token registry — single source of truth for all beskar color tokens.

Each entry is (section, key, attr_name, default_hex).

- section/key: TOML hierarchy and CSS variable naming
- attr_name: Python attribute name in beskar.colors
- default_hex: Factory default color value
"""

from typing import NamedTuple


class Token(NamedTuple):
    section: str
    key: str
    attr: str
    default: str


TOKENS: tuple[Token, ...] = (
    # Surfaces
    Token("surfaces", "base",        "SURFACE_BASE",        "#161616"),
    Token("surfaces", "raised",      "SURFACE_RAISED",      "#1e1e1e"),
    Token("surfaces", "overlay",     "SURFACE_OVERLAY",     "#1a2230"),
    Token("surfaces", "input",       "SURFACE_INPUT",       "#252d3a"),
    Token("surfaces", "dock_header", "SURFACE_DOCK_HEADER", "#161c28"),
    Token("surfaces", "alt",         "SURFACE_ALT",         "#232323"),

    # Borders
    Token("borders", "default",     "BORDER",              "#3a4455"),
    Token("borders", "outer_frame", "BORDER_OUTER_FRAME",  "#323e52"),
    Token("borders", "inner_frame", "BORDER_INNER_FRAME",  "#2a3445"),
    Token("borders", "menu_frame",  "BORDER_MENU_FRAME",   "#3a4455"),
    Token("borders", "hover",       "BORDER_HOVER",        "#344050"),

    # Text
    Token("text", "primary", "TEXT",        "#d0d0d0"),
    Token("text", "bright",  "TEXT_BRIGHT", "#ffffff"),
    Token("text", "slot",    "TEXT_SLOT",   "#b4afa0"),
    Token("text", "label",   "TEXT_LABEL",  "#8c94a0"),
    Token("text", "dim",     "TEXT_DIM",    "#505864"),

    # Accents
    Token("accents", "yellow", "ACCENT_YELLOW", "#ffd100"),
    Token("accents", "blue",   "ACCENT_BLUE",   "#6bb4e6"),
    Token("accents", "link",   "ACCENT_LINK",   "#5aa0e6"),

    # Menus
    Token("menus", "bg",        "MENU_BG",        "#1a2230"),
    Token("menus", "bg_hover",  "MENU_BG_HOVER",  "#252d3a"),
    Token("menus", "border",    "MENU_BORDER",     "#3a4455"),
    Token("menus", "separator", "MENU_SEPARATOR", "#3a4455"),
    Token("menus", "text",      "MENU_TEXT",      "#d0d0d0"),
    Token("menus", "text_dim",  "MENU_TEXT_DIM",  "#505864"),

    # Semantic
    Token("semantic", "highlight",       "HIGHLIGHT",       "#3c78c8"),
    Token("semantic", "selection_green", "SELECTION_GREEN", "#3c7800"),
    Token("semantic", "terminal_green",  "TERMINAL_GREEN",  "#8cc87c"),
    Token("semantic", "button",          "BUTTON",          "#2d2d2d"),
    Token("semantic", "button_text",     "BUTTON_TEXT",     "#d0d0d0"),
)


def defaults() -> dict[str, str]:
    """Return {attr_name: default_hex} for all tokens."""
    return {t.attr: t.default for t in TOKENS}


def key_map() -> dict[str, dict[str, str]]:
    """Return {section: {key: attr_name}} for TOML/override loading."""
    result: dict[str, dict[str, str]] = {}
    for t in TOKENS:
        result.setdefault(t.section, {})[t.key] = t.attr
    return result


def sections() -> list[str]:
    """Return ordered list of unique section names."""
    seen: list[str] = []
    for t in TOKENS:
        if t.section not in seen:
            seen.append(t.section)
    return seen
