"""
Cross-platform compatibility tests for awesome_copilot.cli.

Covers macOS, Linux, and Windows by using pathlib throughout,
tmp_path/monkeypatch.chdir for filesystem isolation, and
mocking _get_agents_dir() so tests don't require an installed wheel.
"""
from __future__ import annotations

import inspect
import re
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

import awesome_copilot.cli as cli_module
from awesome_copilot.cli import _get_agents_dir, install, main


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_fake_agents(base: Path, names: list[str] | None = None) -> Path:
    """Create a fake agents source dir with .agent.md files."""
    if names is None:
        names = ["alpha.agent.md", "beta.agent.md", "gamma.agent.md"]
    agents_dir = base / "src_agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    for name in names:
        (agents_dir / name).write_text(f"---\nname: {name.replace('.agent.md', '')}\n---\n", encoding="utf-8")
    return agents_dir


# ---------------------------------------------------------------------------
# _get_agents_dir()
# ---------------------------------------------------------------------------

class TestGetAgentsDir:
    def test_return_type(self):
        """Always returns Path or None, never raises."""
        result = _get_agents_dir()
        assert result is None or isinstance(result, Path)

    def test_returns_none_when_agents_dir_missing(self, tmp_path):
        """Returns None when the agents/ subdirectory doesn't exist."""
        nonexistent = tmp_path / "agents"
        assert not nonexistent.exists()

        mock_parent = type("_PP", (), {"__truediv__": lambda self, other: nonexistent})()
        mock_path_instance = type("_P", (), {"parent": mock_parent})()
        with patch("awesome_copilot.cli.Path", return_value=mock_path_instance):
            result = _get_agents_dir()
        assert result is None

    def test_returns_none_when_no_agent_files(self, tmp_path):
        """Returns None when agents/ dir exists but has no .agent.md files."""
        empty_agents = tmp_path / "agents"
        empty_agents.mkdir()
        (empty_agents / "readme.txt").write_text("hi")

        mock_parent = type("_PP", (), {"__truediv__": lambda self, other: empty_agents})()
        mock_path_instance = type("_P", (), {"parent": mock_parent})()
        with patch("awesome_copilot.cli.Path", return_value=mock_path_instance):
            result = _get_agents_dir()
        assert result is None

    def test_returns_path_when_agents_present(self, tmp_path):
        """Returns the agents dir when at least one .agent.md exists."""
        agents_dir = tmp_path / "agents"
        agents_dir.mkdir()
        (agents_dir / "test.agent.md").write_text("---\nname: test\n---\n")

        mock_parent = type("_PP", (), {"__truediv__": lambda self, other: agents_dir})()
        mock_path_instance = type("_P", (), {"parent": mock_parent})()
        with patch("awesome_copilot.cli.Path", return_value=mock_path_instance):
            result = _get_agents_dir()
        assert result == agents_dir


# ---------------------------------------------------------------------------
# install()
# ---------------------------------------------------------------------------

class TestInstall:
    def test_creates_github_agents_directory(self, tmp_path, monkeypatch, capsys):
        """install() creates .github/agents/ inside the current working directory."""
        agents_src = _make_fake_agents(tmp_path, ["foo.agent.md"])
        project = tmp_path / "project"
        project.mkdir()
        monkeypatch.chdir(project)

        with patch("awesome_copilot.cli._get_agents_dir", return_value=agents_src):
            install()

        target = project / ".github" / "agents"
        assert target.is_dir()

    def test_copies_all_agent_files(self, tmp_path, monkeypatch, capsys):
        """install() copies every .agent.md file from the source dir."""
        names = ["alpha.agent.md", "beta.agent.md", "gamma.agent.md"]
        agents_src = _make_fake_agents(tmp_path, names)
        project = tmp_path / "project"
        project.mkdir()
        monkeypatch.chdir(project)

        with patch("awesome_copilot.cli._get_agents_dir", return_value=agents_src):
            install()

        for name in names:
            assert (project / ".github" / "agents" / name).exists(), f"{name} not copied"

    def test_copied_files_preserve_content(self, tmp_path, monkeypatch):
        """Copied agent files have byte-for-byte identical content."""
        agents_src = tmp_path / "src_agents"
        agents_src.mkdir()
        content = "---\nname: myagent\ndescription: test\n---\n\nYou are a test agent.\n"
        (agents_src / "myagent.agent.md").write_text(content, encoding="utf-8")

        project = tmp_path / "project"
        project.mkdir()
        monkeypatch.chdir(project)

        with patch("awesome_copilot.cli._get_agents_dir", return_value=agents_src):
            install()

        result = (project / ".github" / "agents" / "myagent.agent.md").read_text(encoding="utf-8")
        assert result == content

    def test_idempotent_run_twice(self, tmp_path, monkeypatch, capsys):
        """Running install() twice doesn't fail or duplicate files."""
        agents_src = _make_fake_agents(tmp_path, ["x.agent.md"])
        project = tmp_path / "project"
        project.mkdir()
        monkeypatch.chdir(project)

        with patch("awesome_copilot.cli._get_agents_dir", return_value=agents_src):
            install()
            install()

        files = list((project / ".github" / "agents").glob("*.agent.md"))
        assert len(files) == 1

    def test_exits_when_no_agents_source(self, tmp_path, monkeypatch):
        """install() calls sys.exit(1) when _get_agents_dir() returns None."""
        project = tmp_path / "project"
        project.mkdir()
        monkeypatch.chdir(project)

        with patch("awesome_copilot.cli._get_agents_dir", return_value=None):
            with pytest.raises(SystemExit) as exc_info:
                install()
        assert exc_info.value.code == 1

    def test_output_lists_filenames(self, tmp_path, monkeypatch, capsys):
        """install() prints each copied filename."""
        names = ["agent-a.agent.md", "agent-b.agent.md"]
        agents_src = _make_fake_agents(tmp_path, names)
        project = tmp_path / "project"
        project.mkdir()
        monkeypatch.chdir(project)

        with patch("awesome_copilot.cli._get_agents_dir", return_value=agents_src):
            install()

        captured = capsys.readouterr().out
        for name in names:
            assert name in captured

    def test_output_includes_count(self, tmp_path, monkeypatch, capsys):
        """install() prints how many agents were installed."""
        names = ["a.agent.md", "b.agent.md"]
        agents_src = _make_fake_agents(tmp_path, names)
        project = tmp_path / "project"
        project.mkdir()
        monkeypatch.chdir(project)

        with patch("awesome_copilot.cli._get_agents_dir", return_value=agents_src):
            install()

        captured = capsys.readouterr().out
        assert "2" in captured

    def test_target_path_uses_cwd(self, tmp_path, monkeypatch):
        """install() always installs relative to cwd, not a hardcoded path."""
        agents_src = _make_fake_agents(tmp_path, ["t.agent.md"])

        project_a = tmp_path / "project_a"
        project_b = tmp_path / "project_b"
        project_a.mkdir()
        project_b.mkdir()

        monkeypatch.chdir(project_a)
        with patch("awesome_copilot.cli._get_agents_dir", return_value=agents_src):
            install()
        assert (project_a / ".github" / "agents" / "t.agent.md").exists()

        monkeypatch.chdir(project_b)
        with patch("awesome_copilot.cli._get_agents_dir", return_value=agents_src):
            install()
        assert (project_b / ".github" / "agents" / "t.agent.md").exists()

    def test_creates_nested_parents(self, tmp_path, monkeypatch):
        """install() creates .github/ and agents/ even if neither exists."""
        agents_src = _make_fake_agents(tmp_path, ["n.agent.md"])
        project = tmp_path / "fresh_project"
        project.mkdir()
        monkeypatch.chdir(project)

        assert not (project / ".github").exists()

        with patch("awesome_copilot.cli._get_agents_dir", return_value=agents_src):
            install()

        assert (project / ".github").is_dir()
        assert (project / ".github" / "agents").is_dir()


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------

class TestMain:
    def test_main_calls_install(self, tmp_path, monkeypatch):
        """main() with no args calls install()."""
        agents_src = _make_fake_agents(tmp_path, ["m.agent.md"])
        project = tmp_path / "project"
        project.mkdir()
        monkeypatch.chdir(project)

        with patch("awesome_copilot.cli._get_agents_dir", return_value=agents_src), \
             patch("sys.argv", ["swe-copilot-agents"]):
            main()

        assert (project / ".github" / "agents" / "m.agent.md").exists()

    def test_version_flag_exits_cleanly(self):
        """--version exits with code 0."""
        with patch("sys.argv", ["swe-copilot-agents", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
        assert exc_info.value.code == 0


# ---------------------------------------------------------------------------
# Cross-platform path safety
# ---------------------------------------------------------------------------

class TestCrossPlatformPaths:
    def test_no_hardcoded_forward_slash_paths(self):
        """Source code must not build paths via string concatenation with '/'."""
        source = inspect.getsource(cli_module)
        # Detect patterns like  "/.github/agents"  or  path + "/agents"
        bad_pattern = re.compile(r'["\'][\w./\\]*/[\w./\\]+["\']')
        matches = bad_pattern.findall(source)
        # Allow only the fixed strings used in print messages, not path construction
        path_strings = [m for m in matches if ".github" in m or "agents/" in m]
        assert not path_strings, f"Hardcoded path strings found: {path_strings}"

    def test_path_objects_used_for_directory_construction(self):
        """install() uses Path / operator, not os.path.join or string ops."""
        source = inspect.getsource(cli_module)
        # Should not use os.path.join for building the target path
        assert "os.path.join" not in source or "github" not in source

    def test_mkdir_uses_parents_flag(self):
        """target_dir.mkdir is called with parents=True for deep path creation."""
        source = inspect.getsource(cli_module)
        assert "parents=True" in source

    def test_mkdir_uses_exist_ok_flag(self):
        """target_dir.mkdir is called with exist_ok=True to avoid race conditions."""
        source = inspect.getsource(cli_module)
        assert "exist_ok=True" in source

    def test_uses_pathlib_path(self):
        """cli module imports and uses pathlib.Path (not os.path)."""
        source = inspect.getsource(cli_module)
        assert "from pathlib import Path" in source

    def test_uses_shutil_copy(self):
        """cli module uses shutil.copy2 for cross-platform file copying."""
        source = inspect.getsource(cli_module)
        assert "shutil.copy2" in source

    def test_target_path_structure(self, tmp_path, monkeypatch):
        """install() puts files at exactly <cwd>/.github/agents/<name>."""
        agents_src = _make_fake_agents(tmp_path, ["s.agent.md"])
        project = tmp_path / "proj"
        project.mkdir()
        monkeypatch.chdir(project)

        with patch("awesome_copilot.cli._get_agents_dir", return_value=agents_src):
            install()

        expected = project / ".github" / "agents" / "s.agent.md"
        assert expected.exists()
        # Verify the path components individually (platform-agnostic)
        parts = expected.relative_to(project).parts
        assert parts == (".github", "agents", "s.agent.md")

    def test_sys_executable_used_in_pth(self):
        """install_prompt.pth uses sys.executable, not a hardcoded python path."""
        pth_path = Path(cli_module.__file__).parent / "install_prompt.pth"
        if not pth_path.exists():
            pytest.skip("install_prompt.pth not present in this installation")
        source = pth_path.read_text(encoding="utf-8")
        assert "sys.executable" in source
        assert "/usr/bin/python" not in source
        assert "C:\\Python" not in source
