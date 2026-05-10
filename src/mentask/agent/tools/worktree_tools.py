<<<<<<< HEAD
=======
import logging
import os
import subprocess

>>>>>>> 5b7fe1d7b7fc6298bf053243e26526fcf13bcdc8
from pydantic import BaseModel, Field

from ...tools.worktree_tools import enter_worktree, exit_worktree
from .base import BaseTool, ToolResult


class WorktreeInput(BaseModel):
    branch_name: str = Field(..., description="The name of the branch to create/use for the worktree")
    base_dir: str = Field(".mentask/worktrees", description="Base directory to store worktrees")


class EnterWorktreeTool(BaseTool):
    """Creates an isolated git worktree for focused mission execution."""

    name = "enter_worktree"
    description = (
        "Creates a git worktree for isolated code modifications. "
        "CRITICAL RULE: DO NOT use this tool for read-only tasks like 'review', 'read', or 'analyze'. "
        "Only use this if you are explicitly asked to write new code, create a feature, or fix a bug."
    )
    input_schema = WorktreeInput
    requires_confirmation = True

    async def execute(self, branch_name: str, base_dir: str = ".mentask/worktrees") -> ToolResult:
        try:
<<<<<<< HEAD
            msg = enter_worktree(branch_name, base_dir)
=======
            # 1. Prepare paths
            repo_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], encoding="utf-8").strip()
            worktree_path = os.path.join(repo_root, base_dir, branch_name)
            os.makedirs(os.path.dirname(worktree_path), exist_ok=True)

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
>>>>>>> 5b7fe1d7b7fc6298bf053243e26526fcf13bcdc8
            return ToolResult(tool_call_id="", content=msg, is_error=False)
        except Exception as e:
            # Preserve the specific fail-fast error so the LLM gets the guardrail message
            is_dirty_error = "ERROR: The working directory is dirty" in str(e)
            content = str(e) if is_dirty_error else f"Error entering worktree: {str(e)}"
            return ToolResult(tool_call_id="", content=content, is_error=True)


class ExitWorktreeTool(BaseTool):
    """Removes a worktree and returns to the main repository root."""

    name = "exit_worktree"
    description = "Exits the current worktree, removes it from git, and returns to the main repository root."

    async def execute(self) -> ToolResult:
        try:
            msg = exit_worktree()
            return ToolResult(tool_call_id="", content=msg, is_error=False)
        except Exception as e:
            return ToolResult(tool_call_id="", content=f"Error exiting worktree: {str(e)}", is_error=True)
