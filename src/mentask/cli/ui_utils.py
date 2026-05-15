"""
Utility functions for gathering system, git, and environment information for the CLI UI.
"""

import os
import random
import subprocess
import sys


def get_ascii_banner() -> str:
    """Returns a wide ASCII banner for MentAsk."""
    return r"""
[bold #4285f4] ███╗   ███╗███████╗███╗   ██╗████████╗ █████╗ ███████╗██╗  ██╗[/]
[bold #8ab4f8] ████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝[/]
[bold #c5a9f5] ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ███████║███████╗█████╔╝ [/]
[bold #a855f7] ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ██╔══██║╚════██║██╔═██╗ [/]
[bold #4c1d95] ██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ██║  ██║███████║██║  ██╗[/]
[bold #4285f4] ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝[/]
[dim] ─────────────────────────────────────────────────────────────────── [/]
[bold white]   THE PYTHON AI AGENT [/][dim]by[/][bold #4285f4] TropicalDev [/]
"""


def get_random_thinking_message() -> str:
    messages = [
        "consulting the ancestors...",
        "downloading more RAM...",
        "centering divs in CSS...",
        "clearing browser history...",
        "convincing the AI not to take over the world...",
        "searching StackOverflow...",
        "reading the documentation...",
        "rebooting the router...",
        "formatting floppy disks...",
        "measuring the flux capacitor...",
        "warming up the quantum engines...",
        "fixing a bug in production...",
        "fighting with the linter...",
        "mining crypto...",
        "evading responsibilities...",
        "calculating the answer to life, the universe and everything...",
        "feeding the server hamsters...",
        "reticulating splines...",
        "compiling the mainframe...",
        "aligning the warp drive...",
        "defragmenting the cloud...",
        "bribing the code monkeys...",
        "turning it off and on again...",
        "updating Adobe Reader...",
        "locating the any key...",
        "rewriting everything in Rust...",
        "exiting Vim...",
        "rm -rf /ing the codebase...",
        "blaming the intern...",
        "resolving merge conflicts in production...",
        "waiting for npm install to finish...",
        "adding more cowbell...",
        "downloading the internet...",
        "decrypting the matrix...",
    ]
    return random.choice(messages)


def get_git_info() -> dict:
    try:
        # Get current branch
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL, encoding="utf-8"
        ).strip()

        # Check for dirty state
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], stderr=subprocess.DEVNULL, encoding="utf-8"
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

    return {"venv": venv_name, "version": version}


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

    return {"name": name, "provider": provider}
