"""Git utilities for PR Summary Generator"""

import os
import subprocess
import typer
from rich import print
from .gemini_utils import generate_commit_message
from .utils import get_branch_name


def get_branch_changes(base_branch: str = "master") -> str:
    """Get all changes that will be included in the PR

    Args:
        base_branch (str): The base branch to compare against (e.g., 'main', 'master', 'develop')
    """
    branch = get_branch_name()
    print(f"[blue]📊 Analyzing changes between {branch} and {base_branch}...[/blue]")

    base = subprocess.run(
        ["git", "merge-base", base_branch, branch], capture_output=True, text=True
    )
    if base.returncode != 0:
        print(
            f"[bold red]Error: Could not find common ancestor with {base_branch}[/bold red]"
        )
        print("[yellow]Tips:[/yellow]")
        print(f"  • Ensure branch {base_branch} exists and is up to date")
        print(f"  • Try running: git fetch origin {base_branch}")
        print("  • Check if you have the correct base branch name")
        raise typer.Exit(1)

    # Get only the code changes, not the commit history
    result = subprocess.run(
        ["git", "diff", base.stdout.strip() + "..HEAD"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("[bold red]Error: Could not get branch changes[/bold red]")
        raise typer.Exit(1)

    # Get list of changed files
    files = subprocess.run(
        ["git", "diff", "--name-status", base.stdout.strip() + "..HEAD"],
        capture_output=True,
        text=True,
    )

    print(f"[green]✓ Found {len(files.stdout.splitlines())} changed files[/green]")

    full_changes = f"""
                Branch Information:
                - Current branch: {branch}
                - Target branch: {base_branch}

                Files Changed:
                {files.stdout}

                Detailed Changes:
                {result.stdout}
                """
    return full_changes


def has_uncommitted_changes() -> bool:
    """Check if there are uncommitted changes in the repository"""
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    return bool(result.stdout.strip())


def group_related_changes() -> list[dict]:
    """Group related changes based on file paths and content"""
    # Get status of all changes
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )

    # Group files by directory and type
    changes = []
    current_group = {"files": [], "diff": "", "type": None}

    for line in result.stdout.splitlines():
        status = line[:2].strip()
        file_path = line[3:].strip()

        # Determine change type
        change_type = "modified"
        if status.startswith("A"):
            change_type = "added"
        elif status.startswith("D"):
            change_type = "deleted"
        elif status.startswith("R"):
            change_type = "renamed"

        # Get diff for this specific file
        diff = subprocess.run(
            ["git", "diff", "--", file_path], capture_output=True, text=True
        ).stdout

        # Start new group if:
        # 1. Different directory
        # 2. Different type of change
        # 3. Unrelated content
        if current_group["files"] and (
            should_start_new_group(current_group, file_path, diff)
            or current_group["type"] != change_type  # Split different change types
        ):
            changes.append(current_group)
            current_group = {"files": [], "diff": "", "type": change_type}

        current_group["files"].append(file_path)
        current_group["diff"] += diff
        current_group["type"] = change_type

    if current_group["files"]:
        changes.append(current_group)

    return changes


def should_start_new_group(current_group: dict, new_file: str, new_diff: str) -> bool:
    """Determine if a new file should start a new group"""
    if not current_group["files"]:
        return False

    current_file = current_group["files"][0]

    # Check if files are in same directory
    current_dir = os.path.dirname(current_file)
    new_dir = os.path.dirname(new_file)

    # Files in different top-level directories should be separate
    if current_dir.split("/")[0] != new_dir.split("/")[0]:
        return True

    # Files with very different content should be separate
    # This is a simple check - could be made more sophisticated
    if not (
        "test" in current_file
        and "test" in new_file
        or "docs" in current_file
        and "docs" in new_file
        or os.path.splitext(current_file)[1] == os.path.splitext(new_file)[1]
    ):
        return True

    return False


def commit_changes(api_key: str) -> None:
    """Commit all changes using AI-generated commit messages"""
    # Group related changes
    change_groups = group_related_changes()

    for group in change_groups:
        # Stage only the files in this group
        for file_path in group["files"]:
            subprocess.run(["git", "add", file_path], check=True)

        # Get detailed information about staged changes
        staged_diff = subprocess.run(
            [
                "git",
                "diff",
                "--staged",
                "--stat",
                "--patch",
            ],  # Added --stat and --patch for more context
            capture_output=True,
            text=True,
        ).stdout

        # Add file context to diff
        files_context = "\n".join(f"• {f}" for f in group["files"])
        diff_with_context = f"""
        Files changed:
        {files_context}
        
        Changes:
        {staged_diff}
        """

        # Generate commit message for this group
        commit_message = generate_commit_message(diff_with_context, api_key)

        # Add change type to commit message if it's not a regular modification
        if group["type"] not in ("modified", None):
            commit_message = f"{group['type']}: {commit_message}"

        # Create commit
        result = subprocess.run(
            ["git", "commit", "-m", commit_message], capture_output=True, text=True
        )

        if result.returncode != 0:
            raise Exception(f"Failed to commit changes: {result.stderr}")

        print(
            f"[green]✓ Created commit for {group['type']} changes: {', '.join(group['files'])}[/green]"
        )


def push_branch() -> None:
    """Push current branch to remote"""
    try:
        # Get current branch name
        branch = get_branch_name()

        # Try to push the branch
        result = subprocess.run(
            ["git", "push", "--set-upstream", "origin", branch],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(f"Failed to push branch: {result.stderr}")

    except Exception as e:
        raise Exception(f"Error pushing branch: {str(e)}")
