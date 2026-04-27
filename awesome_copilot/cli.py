"""
CLI for Awesome Copilot Agents.
"""

import shutil
import sys
from importlib.metadata import version as pkg_version
from pathlib import Path
from typing import Optional


def _get_agents_dir() -> Optional[Path]:
    """Find the agents source directory bundled inside this package."""
    agents_dir = Path(__file__).parent / "agents"
    if agents_dir.exists() and any(agents_dir.glob("*.agent.md")):
        return agents_dir
    return None


def install() -> None:
    """Install agents to .github/agents/ in current directory."""
    agents_dir = _get_agents_dir()
    if not agents_dir:
        print("Error: Could not find agents directory. Try reinstalling: pip install --force-reinstall swe-copilot-agents")
        sys.exit(1)

    target_dir = Path.cwd() / ".github" / "agents"
    target_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for agent_file in sorted(agents_dir.glob("*.agent.md")):
        target_file = target_dir / agent_file.name
        shutil.copy2(agent_file, target_file)
        count += 1
        print(f"  + {agent_file.name}")

    print()
    print(f"Installed {count} agent(s) to {target_dir}")


def main() -> None:
    """Main CLI entry point."""
    import argparse

    try:
        ver = pkg_version("swe-copilot-agents")
    except Exception:
        ver = "unknown"

    parser = argparse.ArgumentParser(
        prog="swe-copilot-agents",
        description="Install GitHub Copilot agents to .github/agents/",
    )
    parser.add_argument("--version", action="version", version=ver)

    parser.parse_args()
    install()


if __name__ == "__main__":
    main()
