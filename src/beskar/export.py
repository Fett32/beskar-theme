"""Export beskar theme tokens to CSS, TOML, and JSON formats.

All exporters read the *current* values from beskar.colors (after overrides),
so they always reflect the active theme.
"""

import json as _json
from pathlib import Path

from beskar.tokens import TOKENS, sections

EXPORTS_DIR = Path.home() / ".config" / "beskar" / "exports"


def _collect() -> dict[str, dict[str, str]]:
    """Collect current token values from beskar.colors, grouped by section."""
    import beskar.colors as c

    result: dict[str, dict[str, str]] = {}
    for t in TOKENS:
        color = getattr(c, t.attr)
        result.setdefault(t.section, {})[t.key] = color.name()
    return result


def export_css(dest: Path | None = None, prefix: str = "beskar") -> Path:
    """Write a CSS custom properties file.

    Output: :root { --beskar-surface-base: #161616; ... }
    """
    dest = dest or EXPORTS_DIR / "beskar.css"
    values = _collect()

    lines = [":root {"]
    for section in sections():
        entries = values.get(section, {})
        if not entries:
            continue
        lines.append(f"  /* {section} */")
        for key, hex_val in entries.items():
            var_name = f"--{prefix}-{section.rstrip('s')}-{key}".replace("_", "-")
            lines.append(f"  {var_name}: {hex_val};")
    lines.append("}")
    lines.append("")

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines))
    return dest


def export_toml(dest: Path | None = None) -> Path:
    """Write a TOML token file."""
    import tomli_w

    dest = dest or EXPORTS_DIR / "beskar-tokens.toml"
    values = _collect()

    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        tomli_w.dump(values, f)
    return dest


def export_json(dest: Path | None = None) -> Path:
    """Write a JSON token file."""
    dest = dest or EXPORTS_DIR / "beskar-tokens.json"
    values = _collect()

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(_json.dumps(values, indent=2) + "\n")
    return dest


def export_all(dest_dir: Path | None = None, prefix: str = "beskar") -> list[Path]:
    """Export all formats to dest_dir. Returns list of written paths."""
    dest_dir = dest_dir or EXPORTS_DIR
    return [
        export_css(dest_dir / "beskar.css", prefix=prefix),
        export_toml(dest_dir / "beskar-tokens.toml"),
        export_json(dest_dir / "beskar-tokens.json"),
    ]
