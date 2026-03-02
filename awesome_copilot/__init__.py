"""
Awesome Copilot Agents - GitHub Copilot custom agents package.

Installation automatically copies agents to your GitHub Copilot directory.
"""

from pathlib import Path
import shutil

__version__ = "0.1.0"


def _install_agents() -> None:
    """Auto-install agents on package import."""
    # Find agents directory (installed via shared-data)
    import sys

    candidates = [
        # Development mode
        Path(__file__).parent.parent / "agents",
        # Installed via pip
        Path(sys.prefix) / "share" / "awesome-copilot" / "agents",
        Path(sys.base_prefix) / "share" / "awesome-copilot" / "agents",
    ]

    agents_dir = None
    for candidate in candidates:
        if candidate.exists() and any(candidate.glob("*.agent.md")):
            agents_dir = candidate
            break

    if not agents_dir:
        return

    # Target directories for GitHub Copilot
    target_dirs = [
        Path.home() / ".github" / "copilot" / "agents",  # VS Code
        Path.home() / ".config" / "github-copilot" / "agents",  # GitHub CLI
    ]

    for target_dir in target_dirs:
        target_dir.mkdir(parents=True, exist_ok=True)
        for agent_file in agents_dir.glob("*.agent.md"):
            target_file = target_dir / agent_file.name
            # Copy if newer or doesn't exist
            if not target_file.exists() or agent_file.stat().st_mtime > target_file.stat().st_mtime:
                shutil.copy2(agent_file, target_file)


# Auto-install on import
_install_agents()


__all__ = ["__version__"]
