"""Filesystem utilities for ai-kit."""

import os
import stat
import importlib.resources
from pathlib import Path
from typing import Optional, List

# Standard project markers in order of preference
WORKSPACE_MARKERS = [".git", ".gitignore", ".cursor", "pyproject.toml", "package.json"]

class WorkspaceError(Exception):
    """Custom exception for workspace-related errors."""

    pass


def remove_file(file_path: Path) -> None:
    """Remove a single file, changing permissions and retrying if needed."""
    try:
        file_path.unlink()
    except PermissionError:
        os.chmod(file_path, stat.S_IWRITE)
        file_path.unlink()
    except FileNotFoundError:
        pass


def remove_dir(dir_path: Path) -> None:
    """Remove a single directory, changing permissions and retrying if needed."""
    try:
        dir_path.rmdir()
    except PermissionError:
        os.chmod(dir_path, stat.S_IWRITE)
        dir_path.rmdir()
    except OSError as e:
        raise e


def remove_tree(root: Path) -> None:
    """Recursively remove a directory tree, handling read-only files/directories."""
    if not root.exists():
        return
    if not root.is_dir():
        raise ValueError(f"{root} is not a directory.")

    # Walk bottom-up
    for dirpath, dirnames, filenames in os.walk(str(root), topdown=False):
        # Remove files first
        for filename in filenames:
            file_path = Path(dirpath) / filename
            remove_file(file_path)

        # Then remove directories
        for dirname in dirnames:
            dir_path = Path(dirpath) / dirname
            remove_dir(dir_path)

    # Finally remove the root folder
    remove_dir(root)


def find_workspace_root(start_path: Optional[Path] = None) -> Path:
    """
    Finds the workspace root by searching for standard project markers starting from
    the given start_path and moving upwards in the directory tree.

    Args:
        start_path (Optional[Path]): The directory to start searching from.
                                      Defaults to the current working directory.

    Returns:
        Path: The workspace root path.

    Raises:
        WorkspaceError: If no workspace root indicators are found in any parent directory.
    """
    if start_path is None:
        current_path = Path.cwd()
    else:
        current_path = start_path.resolve()

    for parent in [current_path] + list(current_path.parents):
        # Check each marker
        for marker in WORKSPACE_MARKERS:
            if (parent / marker).exists():
                return parent

    raise WorkspaceError(
        "Workspace root not found. Ensure you are in a project with standard project markers (.git, .gitignore, pyproject.toml, etc.)"
    )


def join_workspace_path(*args: str) -> Path:
    """
    Joins one or more path components to the workspace root.

    Args:
        *args (str): Path components to join.

    Returns:
        Path: The combined workspace path.

    Raises:
        WorkspaceError: If the workspace root cannot be found.
    """
    workspace_root = find_workspace_root()
    return workspace_root.joinpath(*args).resolve()


def get_relative_path(path: Path) -> Path:
    """
    Gets the relative path from the workspace root to the given path.

    Args:
        path (Path): The absolute path.

    Returns:
        Path: The relative path from the workspace root.

    Raises:
        WorkspaceError: If the workspace root cannot be found.
        ValueError: If the given path is not inside the workspace.
    """
    workspace_root = find_workspace_root()
    try:
        return path.relative_to(workspace_root)
    except ValueError as e:
        raise ValueError(
            f"The path '{path}' is not inside the workspace root '{workspace_root}'."
        ) from e


def ensure_workspace_path(path: Path) -> Path:
    """
    Ensures that the given path is within the workspace. If the path is relative,
    it is made absolute by joining with the workspace root.

    Args:
        path (Path): The path to ensure.

    Returns:
        Path: An absolute path within the workspace.

    Raises:
        WorkspaceError: If the workspace root cannot be found.
    """
    if not path.is_absolute():
        return join_workspace_path(path.parts[0], *path.parts[1:])
    return path


def list_workspace_files(extension: Optional[str] = None) -> list[Path]:
    """
    Lists all files in the workspace. Optionally filters by file extension.

    Args:
        extension (Optional[str]): The file extension to filter by (e.g., '.txt').
                                   If None, all files are listed.

    Returns:
        list[Path]: A list of file paths within the workspace.

    Raises:
        WorkspaceError: If the workspace root cannot be found.
    """
    workspace_root = find_workspace_root()
    if extension:
        return list(workspace_root.rglob(f"*{extension}"))
    return list(workspace_root.rglob("*.*"))


def load_file_content(workspace_path: str) -> str:
    """Load file content from workspace path (relative to workspace root).

    Args:
        workspace_path: Path relative to workspace root

    Returns:
        Content of the file as string

    Raises:
        WorkspaceError: If workspace root cannot be found
        OSError: If file cannot be read
    """
    full_path = join_workspace_path(workspace_path)
    return full_path.read_text()


def package_root() -> Path:
    """Get the root directory of the package."""
    return importlib.resources.files("ai_kit")


def get_filetree(root_dir: str, exclude_dirs: List[str] = None) -> str:
    """
    Generate a markdown file tree for the given root directory.

    Args:
        root_dir: The root directory to generate the tree for.
        exclude_dirs: List of directory names to exclude.

    Returns:
        A string representing the directory tree in markdown format.
    """
    exclude_dirs = exclude_dirs or []
    tree = []
    root_path = Path(root_dir)
    
    def build_tree(current_dir: Path, prefix: str = '', is_last: bool = True):
        entries = sorted(
            current_dir.iterdir(),
            key=lambda e: (not e.is_dir(), e.name)
        )
        entries = [e for e in entries if e.name not in exclude_dirs]
        
        num_entries = len(entries)
        for i, entry in enumerate(entries):
            is_last_entry = i == num_entries - 1
            line_prefix = '└── ' if is_last_entry else '├── '
            if entry.is_dir():
                tree.append(f"{prefix}{line_prefix}{entry.name}/")
                next_prefix = '    ' if is_last_entry else '│   '
                build_tree(entry, prefix + next_prefix, is_last_entry)
            else:
                tree.append(f"{prefix}{line_prefix}{entry.name}")
    
    tree.append(f"{root_path.name}/")
    build_tree(root_path, '', is_last=True)
    
    return '\n'.join(tree)


def crawl_dir(dir_path: str, supported_extensions: List[str]) -> List[tuple[str, str]]:
    paths = []
    dir_path = os.path.abspath(dir_path)
    for root, _, files in os.walk(dir_path):
        for file in files:
            if any(file.lower().endswith(ext.lower()) for ext in supported_extensions):
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, dir_path)
                paths.append((abs_path, rel_path))
    return paths



def load_system_prompt(path: str) -> str:
    """Load a prompt file."""
    from ai_kit.utils.dynamic_file_loader import DynamicFileLoader
    file_loader = DynamicFileLoader()
    return file_loader.load_file_content(path)
