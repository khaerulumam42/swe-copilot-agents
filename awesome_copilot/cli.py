"""
CLI for Awesome Copilot Agents.
"""

import shutil
import sys
from pathlib import Path
from typing import Optional


def _get_agents_dir() -> Optional[Path]:
    """Find the agents source directory."""
    candidates = [
        # Development mode
        Path(__file__).parent.parent / "agents",
        # Installed via pip
        Path(sys.prefix) / "share" / "swe-copilot-agents" / "agents",
        Path(sys.base_prefix) / "share" / "swe-copilot-agents" / "agents",
    ]

    for candidate in candidates:
        if candidate.exists() and any(candidate.glob("*.agent.md")):
            return candidate
    return None


def install() -> None:
    """Install agents to .github/agents/ in current directory."""
    agents_dir = _get_agents_dir()
    if not agents_dir:
        print("❌ Error: Could not find agents directory")
        return

    target_dir = Path.cwd() / ".github" / "agents"
    target_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for agent_file in agents_dir.glob("*.agent.md"):
        target_file = target_dir / agent_file.name
        shutil.copy2(agent_file, target_file)
        count += 1
        print(f"  ✓ {agent_file.name}")

    print()
    print(f"✅ Installed {count} agent(s) to {target_dir}")


def main() -> None:
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="swe-copilot",
        description="Install GitHub Copilot agents to .github/agents/",
    )
    parser.add_argument("--version", action="version", version="0.1.3")

    args = parser.parse_args()
    install()


if __name__ == "__main__":
    main()
