"""Tests for beskar.sanitize — filename safety, path containment, and symlink defense."""

import os
from pathlib import Path

import pytest
import tomli_w

from beskar.sanitize import (
    clean_display_name,
    contained_path,
    safe_filename,
    safe_filename_unique,
)


# ---------------------------------------------------------------------------
# safe_filename
# ---------------------------------------------------------------------------

class TestSafeFilename:
    def test_basic_slug(self):
        assert safe_filename("My Cool Layout") == "my-cool-layout"

    def test_strips_metacharacters(self):
        assert safe_filename("test; rm -rf /") == "test-rm-rf"

    def test_collapses_hyphens(self):
        assert safe_filename("a---b") == "a-b"

    def test_strips_leading_trailing_hyphens(self):
        assert safe_filename("--hello--") == "hello"

    def test_empty_gives_uuid(self):
        result = safe_filename("!!!")
        assert len(result) == 32  # uuid4 hex

    def test_whitespace_only_gives_uuid(self):
        result = safe_filename("   ")
        assert len(result) == 32

    def test_truncates_long_names(self):
        result = safe_filename("a" * 200)
        assert len(result) == 80

    def test_preserves_underscores(self):
        assert safe_filename("my_layout") == "my_layout"

    def test_path_traversal_stripped(self):
        result = safe_filename("../../../etc/passwd")
        assert ".." not in result
        assert "/" not in result

    def test_case_collisions_produce_same_slug(self):
        assert safe_filename("Foo") == safe_filename("foo") == safe_filename("FOO")


# ---------------------------------------------------------------------------
# clean_display_name
# ---------------------------------------------------------------------------

class TestCleanDisplayName:
    def test_clean_input_unchanged(self):
        cleaned, naughty = clean_display_name("My Layout")
        assert cleaned == "My Layout"
        assert naughty is False

    def test_strips_semicolons(self):
        cleaned, naughty = clean_display_name("test; rm -rf /")
        assert ";" not in cleaned
        assert naughty is True

    def test_strips_backticks(self):
        cleaned, naughty = clean_display_name("test `whoami`")
        assert "`" not in cleaned
        assert naughty is True

    def test_strips_dollar(self):
        cleaned, naughty = clean_display_name("$HOME")
        assert "$" not in cleaned
        assert naughty is True

    def test_strips_pipes(self):
        cleaned, naughty = clean_display_name("a | b")
        assert "|" not in cleaned
        assert naughty is True

    def test_strips_control_chars(self):
        cleaned, naughty = clean_display_name("hello\x00world")
        assert "\x00" not in cleaned
        assert naughty is True

    def test_collapses_whitespace(self):
        cleaned, _ = clean_display_name("a    b")
        assert cleaned == "a b"

    def test_preserves_normal_punctuation(self):
        # Periods, commas, slashes, colons are NOT shell metacharacters
        # that we strip (slashes are fine in display names, not filenames)
        cleaned, naughty = clean_display_name("v1.0 test")
        assert cleaned == "v1.0 test"
        assert naughty is False


# ---------------------------------------------------------------------------
# contained_path
# ---------------------------------------------------------------------------

class TestContainedPath:
    def test_normal_child(self, tmp_path):
        child = tmp_path / "subdir" / "file.txt"
        result = contained_path(child, tmp_path)
        assert result == child.resolve()

    def test_rejects_traversal(self, tmp_path):
        escaped = tmp_path / ".." / "etc" / "passwd"
        with pytest.raises(ValueError, match="escapes allowed directory"):
            contained_path(escaped, tmp_path)

    def test_rejects_symlink_outside(self, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        target = outside / "secret.txt"
        target.write_text("secret")

        inside = tmp_path / "profiles"
        inside.mkdir()
        link = inside / "evil.toml"
        link.symlink_to(target)

        with pytest.raises(ValueError, match="escapes allowed directory"):
            contained_path(link, inside)

    def test_allows_symlink_inside(self, tmp_path):
        real = tmp_path / "real.txt"
        real.write_text("ok")
        link = tmp_path / "link.txt"
        link.symlink_to(real)

        result = contained_path(link, tmp_path)
        assert result == real.resolve()


# ---------------------------------------------------------------------------
# safe_filename_unique
# ---------------------------------------------------------------------------

class TestSafeFilenameUnique:
    def test_no_collision(self, tmp_path):
        slug = safe_filename_unique("My Layout", tmp_path, name_key="name")
        assert slug == "my-layout"

    def test_same_display_name_reuses_slug(self, tmp_path):
        # Write a file with the matching display name
        path = tmp_path / "my-layout.toml"
        with open(path, "wb") as f:
            tomli_w.dump({"name": "My Layout"}, f)

        slug = safe_filename_unique("My Layout", tmp_path, name_key="name")
        assert slug == "my-layout"  # reuse, intentional overwrite

    def test_different_display_name_gets_suffix(self, tmp_path):
        # "foo" is taken by a different display name
        path = tmp_path / "foo.toml"
        with open(path, "wb") as f:
            tomli_w.dump({"name": "Foo"}, f)

        slug = safe_filename_unique("FOO!", tmp_path, name_key="name")
        assert slug == "foo-2"

    def test_multiple_collisions(self, tmp_path):
        for i, display in enumerate(["Foo", "Foo?"]):
            suffix = "" if i == 0 else f"-{i + 1}"
            path = tmp_path / f"foo{suffix}.toml"
            with open(path, "wb") as f:
                tomli_w.dump({"name": display}, f)

        slug = safe_filename_unique("foo!!!", tmp_path, name_key="name")
        assert slug == "foo-3"

    def test_dotted_name_key(self, tmp_path):
        path = tmp_path / "test.toml"
        with open(path, "wb") as f:
            tomli_w.dump({"layout": {"name": "Test"}}, f)

        # Same name — reuse
        slug = safe_filename_unique("Test", tmp_path, name_key="layout.name")
        assert slug == "test"

        # Different name — suffix
        slug = safe_filename_unique("Test!", tmp_path, name_key="layout.name")
        assert slug == "test-2"

    def test_no_name_key_skips_collision_check(self, tmp_path):
        path = tmp_path / "foo.toml"
        path.write_text("not even valid toml necessarily")
        slug = safe_filename_unique("foo", tmp_path, name_key=None)
        assert slug == "foo"  # no check, just returns base slug

    def test_symlink_outside_is_skipped(self, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        target = outside / "foo.toml"
        with open(target, "wb") as f:
            tomli_w.dump({"name": "Foo"}, f)

        profiles = tmp_path / "profiles"
        profiles.mkdir()
        link = profiles / "foo.toml"
        link.symlink_to(target)

        # The symlink escapes profiles dir — should be skipped, not read/reused
        slug = safe_filename_unique("Foo", profiles, name_key="name")
        assert slug == "foo-2"  # skipped the symlink, used next candidate

    def test_corrupt_file_is_skipped(self, tmp_path):
        path = tmp_path / "foo.toml"
        path.write_text("this is not valid toml {{{")

        slug = safe_filename_unique("Foo", tmp_path, name_key="name")
        assert slug == "foo-2"  # can't read, don't overwrite
