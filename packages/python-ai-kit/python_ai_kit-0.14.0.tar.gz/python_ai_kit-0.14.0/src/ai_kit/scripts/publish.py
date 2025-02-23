from packaging import version
from rich.console import Console
from pathlib import Path
import subprocess
import sys
from typing import List
import os
import re
import tomli
console = Console()

def get_current_version() -> str:
    """Read current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        raise FileNotFoundError("Cannot find pyproject.toml to read current version.")
    with open(pyproject_path, "rb") as f:
        pyproject = tomli.load(f)
    try:
        return pyproject["tool"]["poetry"]["version"]
    except KeyError:
        raise ValueError("Version not found in pyproject.toml under [tool.poetry.version].")

def run_cmd(cmd: List[str], err_msg: str) -> str:
    """Run a shell command, return stdout or exit on error."""
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.PIPE).strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {err_msg}")
        print(f"Details: {e.stderr or e.output}")
        sys.exit(1)

def get_last_release_tag() -> str:
    """
    Return the highest release tag matching vX.X.X, or an empty string if none.
    """
    # We list only tags matching the pattern vN.N.N
    raw_tags = run_cmd(
        ["git", "tag", "--list", "v[0-9]*.[0-9]*.[0-9]*"],
        "Failed to list tags"
    ).split()
    if not raw_tags:
        return ""

    # Sort them by parsed version and return the highest
    raw_tags.sort(key=lambda t: version.parse(t.lstrip('v')))
    return raw_tags[-1]  # e.g., v0.8.1

def build_and_publish():
    """Build and publish to PyPI"""
    current_version_str = get_current_version()  # e.g. "0.9.0"
    current_version = version.parse(current_version_str)
    tag = f"v{current_version_str}"
    is_dry_run = os.environ.get("DRY_RUN") == "true"

    # 1) If dry run, just print info and exit
    if is_dry_run:
        console.print(f"[yellow]DRY RUN:[/] Would publish version {current_version_str} to PyPI")
        return

    # 2) Check for PyPI credentials
    if "TWINE_USERNAME" not in os.environ or "TWINE_PASSWORD" not in os.environ:
        console.print("[red]Error:[/] PyPI credentials not found in environment")
        sys.exit(1)

    # 3) Compare with last release tag to ensure version was manually bumped
    last_release_tag = get_last_release_tag()
    if last_release_tag:
        last_release_str = last_release_tag.lstrip('v')  # e.g. "0.8.1"
        last_release_version = version.parse(last_release_str)

        # Fail if current version <= last release
        if current_version == last_release_version:
            console.print(f"[yellow]No new release. Current version: {current_version_str}[/]")
            sys.exit(0)
        elif current_version < last_release_version:
            console.print(
                f"[red]Error:[/] Current version {current_version_str} must "
                f"be equal or greater than last release {last_release_str}"
            )
            sys.exit(1)
    else:
        console.print("[yellow]No previous release tags found. Proceeding with first release.[/]")

    # 4) Clean old builds
    for build_path in ["dist", "build"]:
        p = Path(build_path)
        if p.exists():
            run_cmd(["rm", "-rf", build_path], f"Failed to clean {build_path} directory")

    # 5) Build + upload to PyPI + tag
    try:
        run_cmd(["python", "-m", "build"], "Failed to build package")
        run_cmd(["python", "-m", "twine", "upload", "dist/*"], "Failed to upload to PyPI")

        # Create and push tag only after successful upload
        console.print(f"\n[bold cyan]Creating and pushing tag {tag}...[/]")
        run_cmd(["git", "tag", tag], f"Failed to create tag {tag}")
        run_cmd(["git", "push", "--force", "origin", tag], f"Failed to push tag {tag}")

    except Exception as e:
        console.print(f"[red]Error during release: {e}[/]")
        # Clean up tag if it was created
        try:
            subprocess.run(["git", "tag", "-d", tag], check=False)
            subprocess.run(["git", "push", "--force", "origin", f":refs/tags/{tag}"], check=False)
        except:
            pass
        raise


if __name__ == "__main__":
    build_and_publish()
