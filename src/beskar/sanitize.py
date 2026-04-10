"""Shared input-sanitization utilities for the beskar app suite."""

import re
import uuid
from pathlib import Path

# Matches anything that isn't alphanumeric, hyphen, or underscore
_UNSAFE_CHARS = re.compile(r"[^a-z0-9_-]+")
# Collapse repeated hyphens
_MULTI_HYPHEN = re.compile(r"-{2,}")

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
