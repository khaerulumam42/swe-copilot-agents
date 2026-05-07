"""
Tests for agent file validity across all operating systems.

Validates that every .agent.md file in agents/ can be safely used on
macOS, Linux, and Windows — correct encoding, valid filenames, required
YAML frontmatter fields, and safe character sets.
"""
import re
from pathlib import Path

import pytest

AGENTS_DIR = Path(__file__).parent.parent / "agents"
AGENT_FILES = sorted(AGENTS_DIR.glob("*.agent.md"))

# Windows-forbidden characters in filenames (excluding path separators,
# which pathlib handles, but including control chars and special symbols)
_WIN_FORBIDDEN_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

# Windows reserved device names (case-insensitive, with or without extension)
_WIN_RESERVED_NAMES = frozenset({
    "CON", "PRN", "AUX", "NUL",
    "COM0", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT0", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
})

# Valid characters for the agent `name` frontmatter field per spec
_VALID_NAME_CHARS = re.compile(r'^[a-zA-Z0-9._-]+$')


def pytest_generate_tests(metafunc):
    if "agent_file" in metafunc.fixturenames:
        metafunc.parametrize("agent_file", AGENT_FILES, ids=[f.name for f in AGENT_FILES])


# ---------------------------------------------------------------------------
# Collection sanity
# ---------------------------------------------------------------------------

def test_agents_directory_exists():
    assert AGENTS_DIR.is_dir(), f"agents/ directory not found at {AGENTS_DIR}"


def test_at_least_one_agent_exists():
    assert len(AGENT_FILES) > 0, "No .agent.md files found in agents/"


# ---------------------------------------------------------------------------
# Per-file: filename safety
# ---------------------------------------------------------------------------

class TestFilenameCompatibility:
    def test_no_windows_forbidden_chars(self, agent_file):
        """Filename must not contain characters forbidden on Windows."""
        stem = agent_file.name  # e.g. "plan-executor.agent.md"
        assert not _WIN_FORBIDDEN_CHARS.search(stem), (
            f"{stem!r} contains Windows-forbidden characters"
        )

    def test_not_a_windows_reserved_name(self, agent_file):
        """Filename stem must not be a Windows reserved device name."""
        stem_upper = agent_file.stem.upper()  # e.g. "PLAN-EXECUTOR.AGENT"
        # Also check just the first part before the first dot
        first_part = stem_upper.split(".")[0]
        assert first_part not in _WIN_RESERVED_NAMES, (
            f"{agent_file.name!r} conflicts with Windows reserved name {first_part!r}"
        )

    def test_no_trailing_dot_or_space(self, agent_file):
        """Windows rejects filenames ending with a dot or space."""
        name = agent_file.name
        assert not name.endswith("."), f"{name!r} ends with a dot (invalid on Windows)"
        assert not name.endswith(" "), f"{name!r} ends with a space (invalid on Windows)"

    def test_no_spaces_in_filename(self, agent_file):
        """Spaces in filenames cause shell quoting issues across all platforms."""
        assert " " not in agent_file.name, (
            f"{agent_file.name!r} contains spaces — use hyphens instead"
        )

    def test_filename_is_lowercase(self, agent_file):
        """Lowercase names avoid case-sensitivity bugs (Linux is case-sensitive)."""
        assert agent_file.name == agent_file.name.lower(), (
            f"{agent_file.name!r} is not all-lowercase"
        )

    def test_filename_extension_is_agent_md(self, agent_file):
        """Files must use the .agent.md extension."""
        assert agent_file.name.endswith(".agent.md"), (
            f"{agent_file.name!r} does not end with .agent.md"
        )

    def test_filename_length_safe_for_windows(self, agent_file):
        """Filename alone should not exceed Windows MAX_PATH component limit (255 chars)."""
        assert len(agent_file.name) <= 255, (
            f"{agent_file.name!r} exceeds 255-character Windows filename limit"
        )


# ---------------------------------------------------------------------------
# Per-file: encoding
# ---------------------------------------------------------------------------

class TestFileEncoding:
    def test_utf8_readable(self, agent_file):
        """File must be readable as UTF-8 on all platforms."""
        try:
            agent_file.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            pytest.fail(f"{agent_file.name} is not valid UTF-8: {exc}")

    def test_no_null_bytes(self, agent_file):
        """Null bytes corrupt text on all platforms."""
        content = agent_file.read_bytes()
        assert b"\x00" not in content, f"{agent_file.name} contains null bytes"


# ---------------------------------------------------------------------------
# Per-file: YAML frontmatter
# ---------------------------------------------------------------------------

class TestFrontmatter:
    @staticmethod
    def _parse_frontmatter(path: Path) -> dict[str, str]:
        """Extract key: value pairs from the opening --- block."""
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return {}
        end = text.find("---", 3)
        if end == -1:
            return {}
        block = text[3:end].strip()
        result = {}
        for line in block.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                result[key.strip()] = value.strip()
        return result

    def test_has_opening_frontmatter_delimiter(self, agent_file):
        """File must start with --- (YAML frontmatter opening)."""
        text = agent_file.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{agent_file.name} missing opening --- frontmatter"

    def test_has_closing_frontmatter_delimiter(self, agent_file):
        """File must have a closing --- after the opening ---."""
        text = agent_file.read_text(encoding="utf-8")
        assert text.count("---") >= 2, f"{agent_file.name} missing closing --- frontmatter"

    def test_has_description_field(self, agent_file):
        """description: is required by the GitHub Copilot spec."""
        fm = self._parse_frontmatter(agent_file)
        assert "description" in fm, f"{agent_file.name} missing required 'description' field"
        assert fm["description"], f"{agent_file.name} has empty 'description' field"

    def test_name_field_uses_valid_chars(self, agent_file):
        """name: (if present) must only use [a-zA-Z0-9._-]."""
        fm = self._parse_frontmatter(agent_file)
        if "name" not in fm:
            return  # name is optional
        name_val = fm["name"]
        assert _VALID_NAME_CHARS.match(name_val), (
            f"{agent_file.name}: name {name_val!r} contains invalid characters "
            "(only a-z, A-Z, 0-9, ., -, _ are allowed)"
        )

    def test_description_is_not_empty(self, agent_file):
        """description value must not be blank."""
        fm = self._parse_frontmatter(agent_file)
        desc = fm.get("description", "")
        assert desc.strip(), f"{agent_file.name} has a blank description"
