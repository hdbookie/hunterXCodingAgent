import os
import json
import subprocess
import anthropic
from typing import Dict, Any, List

# ============================
# LOAD ENVIRONMENT VARIABLES
# ============================

def load_env_file(filepath: str = ".env"):
    """Load environment variables from .env file."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load .env file if it exists
load_env_file()

# ============================
# ANTHROPIC SETUP
# ============================

client = anthropic.Anthropic()

def anthropic_call(prompt: str) -> str:
    """
    Call Anthropic Claude and return the assistant's raw text.
    Expects JSON like:
    {"action": "tool_name", "args": {...}}
    or {"action": "DONE", "result": "..."}
    """
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract text blocks correctly
    text_chunks = [
        block.text for block in response.content if block.type == "text"
    ]
    return "".join(text_chunks).strip()

def clean_json(raw: str) -> Dict[str, Any]:
    """
    Try to extract JSON from a string in case Claude adds extra text.
    """
    try:
        # Find first { and last }
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON found")

        json_str = raw[start:end]
        return json.loads(json_str)
    except Exception as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {raw}")
        return {"action": "ERROR", "args": {"message": f"Failed to parse JSON: {e}"}}

# ============================
# TOOL DEFINITIONS
# ============================

def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {e}"

def write_file(path: str, contents: str) -> str:
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(contents)
        return f"Successfully wrote {len(contents)} characters to {path}"
    except Exception as e:
        return f"ERROR: {e}"

def edit_file(path: str, line_range: str, new_text: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if ":" in line_range:
            start, end = map(int, line_range.split(":"))
        else:
            start = end = int(line_range)

        # Convert to 0-based indexing
        start_idx = max(0, start - 1)
        end_idx = min(len(lines), end)

        lines[start_idx:end_idx] = [new_text + "\n" if not new_text.endswith("\n") else new_text]

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return f"Successfully edited lines {start}:{end} in {path}"
    except Exception as e:
        return f"ERROR: {e}"

def list_dir(path: str = ".") -> str:
    try:
        items = sorted(os.listdir(path))
        result = []
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                result.append(f"[DIR]  {item}")
            else:
                result.append(f"[FILE] {item}")
        return "\n".join(result)
    except Exception as e:
        return f"ERROR: {e}"

def run_bash(cmd: str, cwd: str = ".") -> str:
    # Expanded allowlist with more useful commands
    allowed = [
        "pytest", "ls", "echo", "cat", "grep", "pwd", "python3", "python",
        "pip", "which", "wc", "head", "tail", "find", "tree", "git status",
        "git diff", "git log", "npm", "node"
    ]

    if not any(cmd.startswith(a) for a in allowed):
        return f"ERROR: Command not allowed: {cmd}. Allowed: {', '.join(allowed)}"

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
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
        return "ERROR: Command timed out after 30 seconds"
    except Exception as e:
        return f"ERROR: {e}"

def grep_search(pattern: str, path: str = ".") -> str:
    try:
        result = subprocess.run(
            ["grep", "-rnI", "--include=*.py", "--include=*.js", "--include=*.ts", pattern, path],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout if result.stdout else "No matches found"
    except Exception as e:
        return f"ERROR: {e}"

def run_python(code: str) -> str:
    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True,
            text=True,
            timeout=15
        )
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}"
        return output or "Python code executed with no output"
    except subprocess.TimeoutExpired:
        return "ERROR: Python code timed out after 15 seconds"
    except Exception as e:
        return f"ERROR: {e}"

# ============================
# TASK MANAGEMENT SYSTEM
# ============================

# Global task storage (resets each run - keeps it simple)
TASKS = []
TASK_COUNTER = 0

def create_task(description: str, priority: str = "medium") -> str:
    """Create a new task with description and priority."""
    global TASK_COUNTER
    TASK_COUNTER += 1

    task = {
        "id": TASK_COUNTER,
        "description": description,
        "status": "pending",
        "priority": priority
    }
    TASKS.append(task)
    return f"Created task #{TASK_COUNTER}: {description}"

def list_tasks() -> str:
    """List all tasks with their current status."""
    if not TASKS:
        return "No tasks created yet"

    result = "Current Tasks:\n" + "=" * 40 + "\n"

    for task in TASKS:
        status_icon = {
            "pending": "☐",
            "in_progress": "🔄",
            "completed": "✅"
        }.get(task["status"], "❓")

        result += f"{status_icon} #{task['id']}: {task['description']} [{task['status']}]\n"

    # Add summary
    pending = len([t for t in TASKS if t["status"] == "pending"])
    in_progress = len([t for t in TASKS if t["status"] == "in_progress"])
    completed = len([t for t in TASKS if t["status"] == "completed"])

    result += f"\nSummary: {pending} pending, {in_progress} in progress, {completed} completed"
    return result

def complete_task(task_id: str) -> str:
    """Mark a task as completed."""
    try:
        task_id_int = int(task_id)
        for task in TASKS:
            if task["id"] == task_id_int:
                task["status"] = "completed"
                return f"✅ Completed task #{task_id}: {task['description']}"
        return f"ERROR: Task #{task_id} not found"
    except ValueError:
        return f"ERROR: Invalid task ID '{task_id}'. Use a number."

def update_task(task_id: str, status: str) -> str:
    """Update task status (pending/in_progress/completed)."""
    valid_statuses = ["pending", "in_progress", "completed"]
    if status not in valid_statuses:
        return f"ERROR: Invalid status '{status}'. Use: {', '.join(valid_statuses)}"

    try:
        task_id_int = int(task_id)
        for task in TASKS:
            if task["id"] == task_id_int:
                old_status = task["status"]
                task["status"] = status
                return f"Updated task #{task_id} from '{old_status}' to '{status}'"
        return f"ERROR: Task #{task_id} not found"
    except ValueError:
        return f"ERROR: Invalid task ID '{task_id}'. Use a number."

# Map tools
TOOLS = {
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "list_dir": list_dir,
    "run_bash": run_bash,
    "grep_search": grep_search,
    "run_python": run_python,
    "create_task": create_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "update_task": update_task,
}

# ============================
# AGENT LOOP
# ============================

SYSTEM_PROMPT = """You are an autonomous coding agent. Your goal is to complete tasks by using tools methodically.

Available tools:
- read_file(path) - Read file contents
- write_file(path, contents) - Write/overwrite a file
- edit_file(path, line_range, new_text) - Edit specific lines (e.g., "5:10" or "5")
- list_dir(path) - List directory contents
- run_bash(cmd) - Run allowed bash commands
- grep_search(pattern, path) - Search for patterns in files
- run_python(code) - Execute Python code
- create_task(description, priority) - Create a new task
- list_tasks() - List all tasks with status
- complete_task(task_id) - Mark a task as completed
- update_task(task_id, status) - Update task status

CRITICAL: Always respond with valid JSON only - ONE ACTION PER RESPONSE:
{"action": "tool_name", "args": {"param": "value"}}
or
{"action": "DONE", "result": "description of what was accomplished"}

For complex tasks, use task management:
1. Start by creating tasks to break down the work
2. Use list_tasks to track progress
3. Work on one task at a time
4. Use complete_task when finishing tasks
5. Take ONE action per response

Think step by step:
1. Understand the goal
2. Check current state (list_dir, read_file)
3. Take actions toward the goal
4. Verify your work
5. When complete, return DONE"""

def run_agent(user_goal: str, max_steps: int = 20, verbose: bool = True):
    """Run the coding agent with the given goal."""

    history = []

    # Initial prompt combining system and user goal
    initial_prompt = f"{SYSTEM_PROMPT}\n\nUSER GOAL: {user_goal}\n\nStart by understanding the current state and then work toward the goal."

    if verbose:
        print(f"🎯 Goal: {user_goal}")
        print("=" * 50)

    for step in range(max_steps):
        if verbose:
            print(f"\n📍 Step {step + 1}")

        # Build prompt from history
        if step == 0:
            prompt = initial_prompt
        else:
            # Build conversation history
            prompt_parts = [SYSTEM_PROMPT, f"GOAL: {user_goal}"]
            for i, h in enumerate(history):
                if h['role'] == 'assistant':
                    prompt_parts.append(f"ASSISTANT: {h['content']}")
                elif h['role'] == 'tool':
                    prompt_parts.append(f"TOOL_RESULT: {h['content']}")
            prompt = "\n\n".join(prompt_parts)

        # Get response from Claude
        raw_resp = anthropic_call(prompt)
        if verbose:
            print(f"🤖 Claude: {raw_resp}")

        # Parse the action
        action = clean_json(raw_resp)

        if action["action"] == "ERROR":
            if verbose:
                print(f"❌ JSON Error: {action.get('args', {}).get('message', 'Unknown error')}")
            history.append({"role": "assistant", "content": raw_resp})
            history.append({"role": "tool", "content": f"JSON parsing failed. Please provide valid JSON."})
            continue

        if action["action"] == "DONE":
            result = action.get("result", "Task completed.")
            if verbose:
                print(f"✅ Completed: {result}")
            return result

        # Execute the tool
        tool_name = action["action"]
        args = action.get("args", {})

        if tool_name not in TOOLS:
            error_msg = f"Unknown tool: {tool_name}. Available: {list(TOOLS.keys())}"
            if verbose:
                print(f"❌ {error_msg}")
            history.append({"role": "assistant", "content": raw_resp})
            history.append({"role": "tool", "content": error_msg})
            continue

        # Run the tool
        try:
            result = TOOLS[tool_name](**args)
            if verbose:
                print(f"🔧 {tool_name}({args}) -> {result[:200]}{'...' if len(result) > 200 else ''}")
        except Exception as e:
            result = f"Tool execution error: {e}"
            if verbose:
                print(f"❌ Tool error: {result}")

        history.append({"role": "assistant", "content": raw_resp})
        history.append({"role": "tool", "content": result})

    return f"Max steps ({max_steps}) reached without completion."

# ============================
# EXAMPLE USAGE
# ============================

if __name__ == "__main__":
    # Example goals to test
    goals = [
        "Create a file hello.py that prints 'Hello, world!' and then run it.",
        "Create a simple calculator.py that can add, subtract, multiply and divide two numbers, then test it.",
        "List the current directory contents and create a README.md file describing what files are present."
    ]

    # Test with the first goal
    goal = goals[0]
    print("🚀 Starting coding agent...")
    result = run_agent(goal, verbose=True)
    print(f"\n🎉 Final result: {result}")