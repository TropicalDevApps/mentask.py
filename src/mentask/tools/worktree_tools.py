import logging
import os
import subprocess

_logger = logging.getLogger("mentask")


def enter_worktree(branch_name: str, base_dir: str = ".mentask/worktrees") -> str:
    """Enters an isolated git worktree."""
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=False)
    if status.stdout.strip():
        raise RuntimeError(
            "ERROR: The working directory is dirty (uncommitted changes exist). "
            "CRITICAL INSTRUCTION: Do NOT attempt to run 'git commit' or 'git stash' yourself. "
            "Stop and ask the user how they want to proceed."
        )

    repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], encoding="utf-8").strip()
    worktree_path = os.path.join(repo_root, base_dir, branch_name)
    os.makedirs(os.path.dirname(worktree_path), exist_ok=True)

    try:
        subprocess.run(["git", "rev-parse", "--verify", branch_name], check=True, capture_output=True)
        cmd = ["git", "worktree", "add", worktree_path, branch_name]
    except subprocess.CalledProcessError:
        cmd = ["git", "worktree", "add", "-b", branch_name, worktree_path]

    subprocess.run(cmd, check=True, capture_output=True, encoding="utf-8")
    os.chdir(worktree_path)

    msg = f"Success: Created and entered worktree at {worktree_path} on branch {branch_name}."
    _logger.info(msg)
    return msg


def exit_worktree() -> str:
    """Exits the current worktree."""
    current_path = os.getcwd()
    repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], encoding="utf-8").strip()

    if current_path == repo_root:
        raise RuntimeError("Already at repository root.")

    os.chdir(repo_root)
    subprocess.run(["git", "worktree", "remove", current_path, "--force"], check=True, capture_output=True)

<<<<<<< HEAD
    msg = f"Success: Exited worktree {current_path} and returned to {repo_root}."
    _logger.info(msg)
    return msg
=======
            # 2. Check if branch exists
            try:
                subprocess.run(["git", "rev-parse", "--verify", branch_name], check=True, capture_output=True)
                # If exists, we just add the worktree for it
                cmd = ["git", "worktree", "add", worktree_path, branch_name]
            except subprocess.CalledProcessError:
                # If not, create a new branch
                cmd = ["git", "worktree", "add", "-b", branch_name, worktree_path]

            # 3. Execute git worktree add
            _ = subprocess.run(cmd, check=True, capture_output=True, encoding="utf-8")

            # 4. Change current working directory to the new worktree
            os.chdir(worktree_path)

            msg = f"Success: Created and entered worktree at {worktree_path} on branch {branch_name}."
            _logger.info(msg)
            return ToolResult(tool_call_id="", content=msg, is_error=False)

        except Exception as e:
            return ToolResult(tool_call_id="", content=f"Error entering worktree: {str(e)}", is_error=True)


class ExitWorktreeTool(BaseTool):
    """Removes a worktree and returns to the main repository root."""

    name = "exit_worktree"
    description = "Exits the current worktree, removes it from git, and returns to the main repository root."

    async def execute(self) -> ToolResult:
        try:
            # 1. Get current worktree path and repo top level
            current_path = os.getcwd()
            repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], encoding="utf-8").strip()

            if current_path == repo_root:
                return ToolResult(tool_call_id="", content="Already at repository root.", is_error=True)

            # 2. Move to repo root
            os.chdir(repo_root)

            # 3. Remove the worktree
            subprocess.run(["git", "worktree", "remove", current_path, "--force"], check=True, capture_output=True)

            msg = f"Success: Exited worktree {current_path} and returned to {repo_root}."
            _logger.info(msg)
            return ToolResult(tool_call_id="", content=msg, is_error=False)

        except Exception as e:
            return ToolResult(tool_call_id="", content=f"Error exiting worktree: {str(e)}", is_error=True)
>>>>>>> 5b7fe1d7b7fc6298bf053243e26526fcf13bcdc8
