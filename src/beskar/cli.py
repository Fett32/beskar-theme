"""CLI entry point for beskar-export."""

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="beskar-export",
        description="Export beskar theme tokens to CSS, TOML, and/or JSON.",
    )
    parser.add_argument(
        "--format",
        choices=["css", "toml", "json", "all"],
        default="all",
        help="Output format (default: all)",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output file path (for single format) or directory (for 'all')",
    )
    parser.add_argument(
        "--prefix",
        default="beskar",
        help="CSS variable prefix (default: beskar)",
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="Load a named profile before exporting",
    )
    args = parser.parse_args()

    # Load profile if requested (copies it to theme.toml position).
    if args.profile:
        profiles_dir = Path.home() / ".config" / "beskar" / "profiles"
        profile_path = profiles_dir / f"{args.profile}.toml"
        if not profile_path.exists():
            print(f"Profile not found: {profile_path}", file=sys.stderr)
            sys.exit(1)
        # Temporarily copy profile to theme.toml so overrides pick it up.
        import shutil
        theme_file = Path.home() / ".config" / "beskar" / "theme.toml"
        theme_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(profile_path, theme_file)

    # Apply overrides (reads theme.toml) before exporting.
    from beskar.overrides import apply_overrides
    apply_overrides()

    from beskar.export import export_css, export_toml, export_json, export_all

    fmt = args.format

    if fmt == "all":
        dest_dir = args.output  # None → default EXPORTS_DIR
        paths = export_all(dest_dir=dest_dir, prefix=args.prefix)
        for p in paths:
            print(p)
    elif fmt == "css":
        path = export_css(dest=args.output, prefix=args.prefix)
        print(path)
    elif fmt == "toml":
        path = export_toml(dest=args.output)
        print(path)
    elif fmt == "json":
        path = export_json(dest=args.output)
        print(path)


if __name__ == "__main__":
    main()
