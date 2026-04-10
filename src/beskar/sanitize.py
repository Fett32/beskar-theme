"""Shared input-sanitization utilities for the beskar app suite."""

import re
import uuid
from pathlib import Path

# Matches anything that isn't alphanumeric, hyphen, or underscore
_UNSAFE_CHARS = re.compile(r"[^a-z0-9_-]+")
# Collapse repeated hyphens
_MULTI_HYPHEN = re.compile(r"-{2,}")
# Shell metacharacters and control chars — anything that could mean
# something special to a shell, IPC command, or config parser
_SHELL_META = re.compile(r"[;|&`$\\\"'<>(){}\[\]!#~\x00-\x1f\x7f]")

MAX_FILENAME_LEN = 80


def safe_filename(name: str) -> str:
    """Turn a user-provided display name into a filesystem-safe slug.

    - Lowercases, replaces spaces with hyphens
    - Strips everything except [a-z0-9_-]
    - Collapses repeated hyphens, strips leading/trailing hyphens
    - Truncates to MAX_FILENAME_LEN characters
    - Falls back to a UUID4 hex string if nothing usable remains
    """
    slug = name.strip().lower().replace(" ", "-")
    slug = _UNSAFE_CHARS.sub("-", slug)
    slug = _MULTI_HYPHEN.sub("-", slug)
    slug = slug.strip("-")
    slug = slug[:MAX_FILENAME_LEN]
    if not slug:
        slug = uuid.uuid4().hex
    return slug


def safe_filename_unique(name: str, directory: Path, name_key: str | None = None,
                         extension: str = ".toml") -> str:
    """Like safe_filename(), but appends -2, -3, ... if the slug already exists
    with a different display name.

    Args:
        name: User-visible display name.
        directory: Where files are stored.
        name_key: TOML key that holds the display name inside the file.
            If None, collision check is skipped (behaves like safe_filename).
        extension: File extension including the dot.

    Returns:
        A slug guaranteed not to collide with a different display name.
    """
    import tomllib

    base = safe_filename(name)
    if name_key is None:
        return base

    candidate = base
    counter = 2
    while True:
        target = directory / f"{candidate}{extension}"
        if not target.exists():
            return candidate
        try:
            with open(target, "rb") as f:
                data = tomllib.load(f)
            # Support dotted keys like "layout.name"
            existing_name = data
            for part in name_key.split("."):
                existing_name = existing_name.get(part, "")
                if not isinstance(existing_name, dict) and part != name_key.split(".")[-1]:
                    existing_name = ""
                    break
            if isinstance(existing_name, str) and existing_name.strip() == name.strip():
                return candidate  # same display name — overwrite is intentional
        except Exception:
            return candidate  # can't read it, just use this slot
        candidate = f"{base}-{counter}"
        counter += 1


def clean_display_name(name: str) -> tuple[str, bool]:
    """Silently strip shell metacharacters and control chars from a display name.

    Returns (cleaned_string, was_naughty) where was_naughty is True if
    anything was stripped.
    """
    cleaned = _SHELL_META.sub("", name)
    cleaned = " ".join(cleaned.split())  # collapse whitespace runs
    return cleaned, cleaned != name


def contained_path(path: Path, root: Path) -> Path:
    """Resolve *path* and verify it lives under *root*.

    Returns the resolved path on success.
    Raises ValueError if the resolved path escapes the root directory.
    """
    resolved = path.resolve()
    root_resolved = root.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError:
        raise ValueError(
            f"Path escapes allowed directory: {resolved} is not under {root_resolved}"
        )
    return resolved
