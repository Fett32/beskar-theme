"""Beskar color tokens — generated from the canonical token registry."""

from PySide6.QtGui import QColor

from beskar.tokens import TOKENS

# Populate module globals from the token registry.
# Each token becomes a module-level QColor (e.g. SURFACE_BASE, BORDER, TEXT).
for _t in TOKENS:
    globals()[_t.attr] = QColor(_t.default)

del _t
