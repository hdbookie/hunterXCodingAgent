"""File and system operations for the Mobile Web Agent."""

import subprocess
from pathlib import Path
from typing import Dict, Any


class FileOperations:
    """Handles all file and system operations."""

    def __init__(self, work_dir: Path):
        self.work_dir = work_dir

    def read_file(self, path: str) -> str:
        """Read file contents relative to work directory."""
        try:
            full_path = self.work_dir / path
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"ERROR: {e}"

    def write_file(self, path: str, contents: str) -> str:
        """Write file contents relative to work directory."""
        try:
            full_path = self.work_dir / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(contents)
            return f"Successfully wrote {len(contents)} characters to {path}"
        except Exception as e:
            return f"ERROR: {e}"

    def edit_file(self, path: str, line_range: str, new_text: str) -> str:
        """Edit specific lines in a file."""
        try:
            full_path = self.work_dir / path
            with open(full_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if ":" in line_range:
                start, end = map(int, line_range.split(":"))
            else:
                start = end = int(line_range)

            start_idx = max(0, start - 1)
            end_idx = min(len(lines), end)

            lines[start_idx:end_idx] = [new_text + "\n" if not new_text.endswith("\n") else new_text]

            with open(full_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return f"Successfully edited lines {start}:{end} in {path}"
        except Exception as e:
            return f"ERROR: {e}"

    def list_dir(self, path: str = ".") -> str:
        """List directory contents relative to work directory."""
        try:
            full_path = self.work_dir / path
            items = sorted(full_path.iterdir())
            result = []
            for item in items:
                if item.is_dir():
                    result.append(f"[DIR]  {item.name}")
                else:
                    result.append(f"[FILE] {item.name}")
            return "\n".join(result)
        except Exception as e:
            return f"ERROR: {e}"

    def run_bash(self, cmd: str, cwd: str = ".") -> str:
        """Run bash command in work directory with safety restrictions."""
        # Enhanced allowlist for mobile development
        allowed = [
            "npm", "yarn", "pnpm", "node", "python3", "python", "pip",
            "git", "ls", "echo", "cat", "grep", "pwd", "which", "wc", "head", "tail",
            "find", "tree", "jest", "playwright", "cypress", "lighthouse",
            "mkdir", "touch", "rm", "cp", "mv", "chmod"
        ]

        if not any(cmd.startswith(a) for a in allowed):
            return f"ERROR: Command not allowed: {cmd}. Allowed: {', '.join(allowed)}"

        try:
            full_cwd = self.work_dir / cwd
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=full_cwd,
                capture_output=True,
                text=True,
                timeout=60
            )
            output = ""
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}"
            if result.returncode != 0:
                output += f"Return code: {result.returncode}"
            return output or "Command completed with no output"
        except subprocess.TimeoutExpired:
            return "ERROR: Command timed out after 60 seconds"
        except Exception as e:
            return f"ERROR: {e}"

    def grep_search(self, pattern: str, path: str = ".") -> str:
        """Search for patterns in files."""
        try:
            full_path = self.work_dir / path
            result = subprocess.run(
                ["grep", "-rnI", "--include=*.py", "--include=*.js", "--include=*.ts",
                 "--include=*.tsx", "--include=*.jsx", "--include=*.html", "--include=*.css", pattern, str(full_path)],
                capture_output=True,
                text=True,
                timeout=15
            )
            return result.stdout if result.stdout else "No matches found"
        except Exception as e:
            return f"ERROR: {e}"