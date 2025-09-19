"""Reflection and assessment system for the Mobile Web Agent."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .file_operations import FileOperations
    from .task_manager import TaskManager


class ReflectionSystem:
    """Handles agent self-reflection and assessment."""

    def __init__(self, file_ops: "FileOperations", task_manager: "TaskManager", prd_tracker=None):
        self.file_ops = file_ops
        self.task_manager = task_manager
        self.prd_tracker = prd_tracker

    def reflect_and_assess(self, focus: str = "overall") -> str:
        """Reflect on recent progress and assess current state."""
        try:
            # Get current state
            task_summary = self.task_manager.list_tasks()

            if self.prd_tracker and self.prd_tracker.prd:
                progress_dashboard = self.prd_tracker.generate_progress_dashboard()
                next_priorities = self.prd_tracker.get_next_priorities()
            else:
                progress_dashboard = "No PRD loaded"
                next_priorities = []

            # Analyze current directory structure
            current_files = self.file_ops.list_dir(".")

            reflection = f"""
🔍 REFLECTION AND ASSESSMENT
{'=' * 40}

CURRENT TASK STATUS:
{task_summary}

PRD PROGRESS:
{progress_dashboard}

CURRENT PROJECT STATE:
{current_files}

NEXT PRIORITIES:
"""
            for i, priority in enumerate(next_priorities[:5], 1):
                reflection += f"{i}. {priority}\n"

            reflection += f"""
ASSESSMENT QUESTIONS:
- Are we making progress toward PRD goals? {"Yes" if self.prd_tracker and self.prd_tracker.prd else "No PRD loaded"}
- Are there any blocking issues in recent actions?
- Do we have proper project structure in place?
- Are tests set up and passing?
- Is the current approach working effectively?

RECOMMENDATIONS:
"""

            # Basic heuristics for recommendations
            if "No PRD loaded" in progress_dashboard:
                reflection += "- CRITICAL: Load PRD file first to guide development\n"

            if "package.json" not in current_files and "No files found" not in current_files:
                reflection += "- Consider setting up project structure (package.json, src/, etc.)\n"

            pending_tasks = len([t for t in self.task_manager.tasks if t["status"] == "pending"])
            in_progress_tasks = len([t for t in self.task_manager.tasks if t["status"] == "in_progress"])

            if in_progress_tasks > 1:
                reflection += "- Focus: Complete current in-progress tasks before starting new ones\n"
            elif pending_tasks == 0 and in_progress_tasks == 0:
                reflection += "- Create specific tasks based on PRD requirements\n"

            reflection += "\nREFLECTION COMPLETE - Ready to continue development."

            return reflection

        except Exception as e:
            return f"ERROR during reflection: {e}"