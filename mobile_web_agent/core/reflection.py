"""Reflection and assessment system for the Mobile Web Agent."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .file_operations import FileOperations
    from .task_manager import TaskManager
    from .code_critic import CodeCritic


class ReflectionSystem:
    """Handles agent self-reflection and assessment."""

    def __init__(self, file_ops: "FileOperations", task_manager: "TaskManager", prd_tracker=None, code_critic: "CodeCritic" = None):
        self.file_ops = file_ops
        self.task_manager = task_manager
        self.prd_tracker = prd_tracker
        self.code_critic = code_critic

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

            # Add code quality assessment if critic is available
            if self.code_critic and focus in ["overall", "code_quality"]:
                reflection += "\nCODE QUALITY ASSESSMENT:\n"

                # Get recently modified Python files
                python_files = []
                try:
                    all_files = self.file_ops.list_dir(".", recursive=True)
                    python_files = [f for f in all_files.split('\n') if f.strip().endswith('.py') and f.strip()]
                except:
                    pass

                if python_files:
                    quality_summary = {"total_files": 0, "average_score": 0, "critical_issues": 0}

                    for file_path in python_files[:5]:  # Limit to 5 most recent files
                        try:
                            file_content = self.file_ops.read_file(file_path.strip())
                            if file_content and not file_content.startswith("ERROR"):
                                critique = self.code_critic.critique_code(file_content, file_path.strip())
                                quality_summary["total_files"] += 1
                                quality_summary["average_score"] += critique["quality_score"]
                                quality_summary["critical_issues"] += critique["severity_breakdown"]["critical"]
                        except:
                            continue

                    if quality_summary["total_files"] > 0:
                        quality_summary["average_score"] /= quality_summary["total_files"]
                        reflection += f"- Files analyzed: {quality_summary['total_files']}\n"
                        reflection += f"- Average quality score: {quality_summary['average_score']:.1f}/100\n"
                        reflection += f"- Critical issues found: {quality_summary['critical_issues']}\n"

                        if quality_summary["critical_issues"] > 0:
                            reflection += "- ⚠️  CRITICAL: Address security and syntax issues immediately\n"
                        elif quality_summary["average_score"] < 70:
                            reflection += "- 📈 Recommendation: Focus on code quality improvements\n"
                        else:
                            reflection += "- ✅ Code quality is acceptable\n"
                else:
                    reflection += "- No Python files found for analysis\n"

            reflection += "\nREFLECTION COMPLETE - Ready to continue development."

            return reflection

        except Exception as e:
            return f"ERROR during reflection: {e}"

    def assess_code_quality(self, file_path: str) -> str:
        """Perform detailed code quality assessment for a specific file."""
        if not self.code_critic:
            return "Code critic not available"

        try:
            file_content = self.file_ops.read_file(file_path)
            if file_content.startswith("ERROR"):
                return f"Could not read file: {file_content}"

            critique = self.code_critic.critique_code(file_content, file_path)

            assessment = f"""
🔍 CODE QUALITY ASSESSMENT: {file_path}
{'=' * 50}

QUALITY SCORE: {critique['quality_score']}/100
OVERALL: {critique['overall_assessment']}

ISSUES FOUND: {critique['total_issues']}
- Critical: {critique['severity_breakdown']['critical']}
- High: {critique['severity_breakdown']['high']}
- Medium: {critique['severity_breakdown']['medium']}
- Low: {critique['severity_breakdown']['low']}

RECOMMENDATIONS:
"""
            for rec in critique['recommendations']:
                assessment += f"  {rec}\n"

            if critique['issues_by_category']:
                assessment += "\nTOP ISSUES BY CATEGORY:\n"
                for category, issues in list(critique['issues_by_category'].items())[:3]:
                    assessment += f"\n{category.upper()}:\n"
                    for issue in issues[:2]:  # Show top 2 issues per category
                        line_info = f" (line {issue['line']})" if issue['line'] else ""
                        assessment += f"  • {issue['message']}{line_info}\n"
                        assessment += f"    → {issue['suggestion']}\n"

            return assessment

        except Exception as e:
            return f"ERROR during code quality assessment: {e}"