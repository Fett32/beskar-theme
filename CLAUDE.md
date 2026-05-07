# beskar-theme

PySide6 color/palette/stylesheet system used by every Manda* app. Pip package, module name `beskar`. Stable; touch carefully because six downstream projects break on token churn.

## Layout

- `src/beskar/tokens.py` — **canonical token registry** (single source of truth). All other files derive from `TOKENS`.
- `src/beskar/colors.py` — module-level `QColor` constants generated from `TOKENS` at import.
- `src/beskar/palette.py` — `make_palette()` returns a Qt `QPalette` (hardcoded values, predates `tokens.py`; safe to leave alone).
- `src/beskar/stylesheet.py` — small QSS helpers: `button()`, `input_field()`, `dialog()`, `scrollbar()`. Hex values are hardcoded — if a token changes, update here too.
- `src/beskar/overrides.py` — reads `~/.config/beskar/theme.toml`, patches `beskar.colors` globals. `apply_overrides()` is called from `__init__.py` on import.
- `src/beskar/export.py` — writes CSS / TOML / JSON to `~/.config/beskar/exports/`.
- `src/beskar/cli.py` — `beskar-export` entry point. Supports `--profile NAME` to load from `~/.config/beskar/profiles/`.
- `src/beskar/sanitize.py` — **shared suite utilities** (filename safety, symlink containment). MandaSpace and MandaVM depend on this; treat as load-bearing.
- `tests/test_sanitize.py` — only test file. Token registry + overrides are uncovered.

## Dependents (don't break these)

- `beskar-studio` — Python, full surface
- MandaNote, MandaReel, MandaTrip — Python, `beskar.colors` + `make_palette`
- MandaSpace, MandaVM — Python, `beskar.sanitize` (filename/path safety)
- MandaForge — Web/Tauri, consumes the exported `beskar.css` via symlink

## Workflow rules

- **Adding/renaming a token:** edit `TOKENS` in `tokens.py`, then `beskar-export --format all` to regenerate the CSS/TOML/JSON consumers read. Sweep `stylesheet.py` for hardcoded hex matches. Then sweep dependent projects.
- **`stylesheet.py` is not generated** — its hex values are independent strings. Always manually mirror token changes here.
- The `beskar.colors` module has runtime globals (no static `SURFACE_BASE = QColor(...)` lines). IDE jumps won't find the definition; look at `tokens.py`.
- `apply_overrides()` runs automatically on `import beskar`. Tests that mock `~/.config/beskar/` should patch `_THEME_FILE` in `overrides.py`.

## Palette identity

Dark navy / blue-grey dominant, mid-blue highlights, yellow as a tiny accent. Do not propose "yellow + dark" Beskar visuals. `#FFD100` is OSHA hazard yellow used elsewhere — coincidence, not brand.

## Status

Clean on `main`, last commit 2026-04-19. No open branches.
