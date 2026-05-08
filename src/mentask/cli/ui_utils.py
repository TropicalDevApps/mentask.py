"""
Utility functions for gathering system, git, and environment information for the CLI UI.
"""

import os
import subprocess
import sys


def get_git_info() -> dict:
    """Returns a dictionary with git branch and status information."""
    try:
        # Get current branch
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], 
            stderr=subprocess.DEVNULL, 
            encoding="utf-8"
        ).strip()
        
        # Check for dirty state
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], 
            stderr=subprocess.DEVNULL, 
            encoding="utf-8"
        ).strip()
        
        is_dirty = len(status) > 0
        return {"branch": branch, "is_dirty": is_dirty}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"branch": None, "is_dirty": False}


def get_python_info() -> dict:
    """Returns information about the current Python environment."""
    venv = os.environ.get("VIRTUAL_ENV") or os.environ.get("CONDA_DEFAULT_ENV")
    venv_name = os.path.basename(venv) if venv else None
    
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    
    return {
        "venv": venv_name,
        "version": version
    }


def get_model_info(model_id: str) -> dict:
    """Simplifies model ID for display."""
    if not model_id:
        return {"name": "unknown", "provider": "unknown"}
    
    parts = model_id.split("/")
    name = parts[-1]
    provider = parts[0] if len(parts) > 1 else "google"
    
    # Common shorteners
    name = name.replace("gemini-", "gem-")
    name = name.replace("claude-", "c-")
    name = name.replace("-latest", "")
    
    return {
        "name": name,
        "provider": provider
    }
