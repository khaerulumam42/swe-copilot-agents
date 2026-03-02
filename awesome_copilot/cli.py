"""
CLI for Awesome Copilot Agents.

Provides install and update commands to manage GitHub Copilot custom agents.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


def get_agents_source_dir() -> Path:
    """
    Find the agents source directory in the installed package.

    The agents are installed via shared-data to:
    - <prefix>/share/awesome-copilot/agents

    Returns:
        Path to the agents directory.
    """
    # Try multiple possible locations for the agents
    candidates = []

    # 1. Check if we're in development mode (running from source)
    dev_dir = Path(__file__).parent.parent / "agents"
    if dev_dir.exists():
        return dev_dir

    # 2. Check sys.prefix for installed package data (most common)
    # pip install: <venv>/share/awesome-copilot/agents
    # system install: /usr/local/share/awesome-copilot/agents
    base_dir = Path(sys.prefix)
    candidates.append(base_dir / "share" / "awesome-copilot" / "agents")

    # 3. Check base prefix for virtual environments
    if hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix:
        base_dir = Path(sys.base_prefix)
        candidates.append(base_dir / "share" / "awesome-copilot" / "agents")

    # 4. Check the package's installed location (for editable installs)
    # This handles: pip install -e .
    pkg_dir = Path(__file__).parent.parent
    candidates.append(pkg_dir / "agents")

    # 5. Check common data directories on various systems
    if sys.platform == "darwin":
        # macOS: /usr/local/share, /Library/Application Support
        candidates.extend([
            Path("/usr/local/share/awesome-copilot/agents"),
            Path("/Library/Application Support/awesome-copilot/agents"),
        ])
    elif sys.platform == "linux":
        # Linux: /usr/share, /usr/local/share, ~/.local/share
        candidates.extend([
            Path("/usr/share/awesome-copilot/agents"),
            Path("/usr/local/share/awesome-copilot/agents"),
            Path.home() / ".local" / "share" / "awesome-copilot" / "agents",
        ])
    elif sys.platform == "win32":
        # Windows: AppData/Local, ProgramData
        candidates.extend([
            Path(os.environ.get("LOCALAPPDATA", "")) / "awesome-copilot" / "agents",
            Path(os.environ.get("PROGRAMDATA", "")) / "awesome-copilot" / "agents",
        ])

    # Return the first existing directory
    for candidate in candidates:
        if candidate.exists() and any(candidate.glob("*.agent.md")):
            return candidate

    # If nothing found, raise an informative error
    raise FileNotFoundError(
        f"Could not find agents directory. Searched:\n" +
        "\n".join(f"  - {c}" for c in candidates) +
        "\n\nTry reinstalling the package: pip install --force-reinstall awesome-copilot-agents"
    )


# Source agents directory (computed at import time)
try:
    AGENTS_SOURCE_DIR = get_agents_source_dir()
except FileNotFoundError:
    AGENTS_SOURCE_DIR = None

# Target directory where GitHub Copilot looks for custom agents
# VS Code Desktop: ~/.github/copilot/agents
# GitHub CLI: ~/.config/github-copilot/agents
AGENT_TARGET_DIRS = [
    Path.home() / ".github" / "copilot" / "agents",  # VS Code / GitHub Desktop
    Path.home() / ".config" / "github-copilot" / "agents",  # GitHub CLI
]


def get_target_dir() -> Path | None:
    """Find the first existing GitHub Copilot agents directory."""
    for target_dir in AGENT_TARGET_DIRS:
        if target_dir.exists() or target_dir.parent.exists():
            return target_dir
    # Default to VS Code location
    return AGENT_TARGET_DIRS[0]


def install_agents(target_dir: Path | None = None) -> bool:
    """
    Copy agents to user's GitHub Copilot directory.

    Args:
        target_dir: Optional target directory. If not provided, auto-detects.

    Returns:
        True if successful, False otherwise.
    """
    target_dir = target_dir or get_target_dir()

    # Resolve agents directory
    try:
        agents_dir = get_agents_source_dir()
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return False

    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy all agent files
    agent_files = list(agents_dir.glob("*.agent.md"))
    if not agent_files:
        print("⚠️  Warning: No agent files found in agents directory")
        return False

    print(f"📦 Installing agents to: {target_dir}")
    print()

    for agent_file in agent_files:
        target_file = target_dir / agent_file.name
        shutil.copy2(agent_file, target_file)
        print(f"  ✓ {agent_file.name}")

    print()
    print(f"✅ Successfully installed {len(agent_files)} agent(s)")
    print(f"   Location: {target_dir}")
    return True


def update_agents() -> bool:
    """
    Update agents from the latest installed version.

    This is essentially the same as install - it overwrites existing agents.

    Returns:
        True if successful, False otherwise.
    """
    return install_agents()


def list_agents() -> bool:
    """List all available agents in the package."""
    try:
        agents_dir = get_agents_source_dir()
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return False

    agent_files = list(agents_dir.glob("*.agent.md"))
    if not agent_files:
        print("No agent files found")
        return False

    print("Available agents:")
    print()
    for agent_file in sorted(agent_files):
        # Extract name from frontmatter
        try:
            content = agent_file.read_text()
            name = agent_file.stem.replace("-", " ").replace("_", " ").title()
            print(f"  • @{agent_file.stem}")
        except Exception:
            print(f"  • {agent_file.name}")

    return True


def show_status() -> bool:
    """Show installation status."""
    target_dir = get_target_dir()

    # Import version from package
    try:
        from importlib.metadata import version
        pkg_version = version("awesome-copilot-agents")
    except Exception:
        pkg_version = "unknown"

    # Get agents directory for display
    try:
        agents_dir = get_agents_source_dir()
        agents_dir_str = str(agents_dir)
    except FileNotFoundError:
        agents_dir_str = "Not found (try reinstalling)"

    print("GitHub Copilot Agents Status")
    print("=" * 40)
    print(f"Package version: {pkg_version}")
    print(f"Source directory: {agents_dir_str}")
    print(f"Target directory: {target_dir}")
    print()

    if target_dir.exists():
        installed = list(target_dir.glob("*.agent.md"))
        print(f"Installed agents: {len(installed)}")
        for agent in sorted(installed):
            print(f"  • {agent.name}")
    else:
        print("No agents installed yet")
        print(f"  Run 'awesome-copilot install' to install")

    return True


def main() -> None:
    """Main CLI entry point."""
    # Get package version
    try:
        from importlib.metadata import version
        pkg_version = version("awesome-copilot-agents")
    except Exception:
        pkg_version = "0.1.0"

    parser = argparse.ArgumentParser(
        prog="awesome-copilot",
        description="Manage GitHub Copilot custom agents",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {pkg_version}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Install command
    subparsers.add_parser(
        "install",
        help="Install agents to GitHub Copilot directory",
    )

    # Update command
    subparsers.add_parser(
        "update",
        help="Update installed agents to latest version",
    )

    # List command
    subparsers.add_parser(
        "list",
        help="List all available agents",
    )

    # Status command
    subparsers.add_parser(
        "status",
        help="Show installation status",
    )

    args = parser.parse_args()

    if args.command == "install":
        success = install_agents()
        exit(0 if success else 1)

    elif args.command == "update":
        success = update_agents()
        exit(0 if success else 1)

    elif args.command == "list":
        success = list_agents()
        exit(0 if success else 1)

    elif args.command == "status":
        success = show_status()
        exit(0 if success else 1)

    else:
        parser.print_help()
        exit(0)


if __name__ == "__main__":
    main()
