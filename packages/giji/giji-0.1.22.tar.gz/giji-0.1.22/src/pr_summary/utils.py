"""Shared utilities for PR Summary Generator"""

import re
import subprocess
from typing import Optional


def get_branch_name() -> str:
    """Get the current branch name"""
    result = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True
    )
    return result.stdout.strip()


def extract_ticket_from_branch(branch_name: str) -> Optional[str]:
    """
    Extract ticket number from branch name.

    Supported formats:
    - SIS-123
    - SIS-123/description
    - type/SIS-123-description
    - feature/SIS-123/new-feature
    - fix/SIS-123
    """
    # Pattern matches SIS-XXX in various formats
    patterns = [
        r"^SIS-\d+$",  # SIS-123
        r"^SIS-\d+/",  # SIS-123/description
        r"/SIS-\d+",  # type/SIS-123 or type/SIS-123-description
        r"^[^/]+/SIS-\d+",  # feature/SIS-123
    ]

    for pattern in patterns:
        match = re.search(pattern, branch_name)
        if match:
            # Extract just the SIS-XXX part
            ticket_match = re.search(r"SIS-\d+", match.group(0))
            if ticket_match:
                return ticket_match.group(0)

    return None
