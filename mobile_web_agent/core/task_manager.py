"""Task management system for the Mobile Web Agent."""

from typing import Dict, List, Any


class TaskManager:
    """Manages tasks and progress tracking."""

    def __init__(self):
        self.tasks: List[Dict[str, Any]] = []
        self.task_counter = 0

    def create_task(self, description: str, priority: str = "medium") -> str:
        """Create a new task with description and priority."""
        self.task_counter += 1
        task = {
            "id": self.task_counter,
            "description": description,
            "status": "pending",
            "priority": priority
        }
        self.tasks.append(task)
        return f"Created task #{self.task_counter}: {description}"

    def list_tasks(self) -> str:
        """List all tasks with their current status."""
        if not self.tasks:
            return "No tasks created yet"

        result = "Current Tasks:\n" + "=" * 40 + "\n"
        for task in self.tasks:
            status_icon = {
                "pending": "☐",
                "in_progress": "🔄",
                "completed": "✅"
            }.get(task["status"], "❓")
            result += f"{status_icon} #{task['id']}: {task['description']} [{task['status']}]\n"

        pending = len([t for t in self.tasks if t["status"] == "pending"])
        in_progress = len([t for t in self.tasks if t["status"] == "in_progress"])
        completed = len([t for t in self.tasks if t["status"] == "completed"])

        result += f"\nSummary: {pending} pending, {in_progress} in progress, {completed} completed"
        return result

    def complete_task(self, task_id: str) -> str:
        """Mark a task as completed."""
        try:
            task_id_int = int(task_id)
            for task in self.tasks:
                if task["id"] == task_id_int:
                    task["status"] = "completed"
                    return f"✅ Completed task #{task_id}: {task['description']}"
            return f"ERROR: Task #{task_id} not found"
        except ValueError:
            return f"ERROR: Invalid task ID '{task_id}'. Use a number."

    def update_task(self, task_id: str, status: str) -> str:
        """Update task status."""
        valid_statuses = ["pending", "in_progress", "completed"]
        if status not in valid_statuses:
            return f"ERROR: Invalid status '{status}'. Use: {', '.join(valid_statuses)}"

        try:
            task_id_int = int(task_id)
            for task in self.tasks:
                if task["id"] == task_id_int:
                    old_status = task["status"]
                    task["status"] = status
                    return f"Updated task #{task_id} from '{old_status}' to '{status}'"
            return f"ERROR: Task #{task_id} not found"
        except ValueError:
            return f"ERROR: Invalid task ID '{task_id}'. Use a number."