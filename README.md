# Coding Agent

A minimal, autonomous coding agent built from scratch using Claude (Anthropic). This agent can read/write files, run bash commands, and iteratively work toward goals without step-by-step instructions.

## 🎯 What It Does

The agent follows the **LLM + Tools + Loop** pattern:
- **LLM**: Claude for reasoning and decision-making
- **Tools**: File operations, bash commands, Python execution, code search
- **Loop**: Autonomous iteration until task completion

## 🔧 Features

### Core Tools
- **File Operations**: `read_file`, `write_file`, `edit_file`
- **System**: `run_bash`, `list_dir`, `grep_search`
- **Code Execution**: `run_python` for testing snippets

### Safety Features
- Allowlisted bash commands only
- Timeouts for all operations
- Robust error handling
- JSON communication validation

## 🚀 Quick Start

1. **Setup**:
   ```bash
   python3 setup.py
   source agent_env/bin/activate  # If new venv was created
   export ANTHROPIC_API_KEY="your_api_key_here"
   ```

2. **Run**:
   ```bash
   python3 coding_agent.py
   ```

3. **Example Goals**:
   - "Create a hello.py file that prints 'Hello, world!' and run it"
   - "Build a simple calculator with add/subtract/multiply/divide functions"
   - "Analyze the current directory and create documentation"

## 🎨 Design Philosophy

- **Autonomous**: Runs independently, returns with results
- **Iterative**: Learns from mistakes and improves
- **Fast**: Optimized for quick MVP generation and testing
- **Safe**: Restricted operations with proper error handling

## 🔍 How It Works

1. **Goal Setting**: You provide a high-level objective
2. **State Analysis**: Agent explores current environment
3. **Action Planning**: Decides on next steps using available tools
4. **Execution**: Performs actions and observes results
5. **Iteration**: Repeats until goal is achieved or max steps reached

## 🛠 Customization

### Adding New Tools
```python
def my_custom_tool(param: str) -> str:
    # Your tool logic here
    return result

# Add to TOOLS dictionary
TOOLS["my_custom_tool"] = my_custom_tool
```

### Adjusting Behavior
- Modify `max_steps` for longer/shorter runs
- Update `SYSTEM_PROMPT` for different personalities
- Extend `allowed` commands in `run_bash` for more capabilities

## 📋 Requirements

- Python 3.8+
- Anthropic API key
- `anthropic` package (auto-installed by setup)

## 🔒 Security

- Bash commands are allowlisted
- File operations are sandboxed to current directory
- All operations have timeouts
- No network access beyond Anthropic API

## 🎯 Example Session

```
🎯 Goal: Create a hello.py file that prints 'Hello, world!' and then run it.
==================================================

📍 Step 1
🤖 Claude: {"action": "list_dir", "args": {}}
🔧 list_dir({}) -> [FILE] README.md
[FILE] coding_agent.py
[FILE] requirements.txt
[FILE] setup.py

📍 Step 2
🤖 Claude: {"action": "write_file", "args": {"path": "hello.py", "contents": "print('Hello, world!')"}}
🔧 write_file({'path': 'hello.py', 'contents': "print('Hello, world!')"}) -> Successfully wrote 20 characters to hello.py

📍 Step 3
🤖 Claude: {"action": "run_python", "args": {"code": "exec(open('hello.py').read())"}}
🔧 run_python({'code': "exec(open('hello.py').read())"}) -> STDOUT:
Hello, world!

📍 Step 4
🤖 Claude: {"action": "DONE", "result": "Successfully created hello.py file that prints 'Hello, world!' and confirmed it runs correctly."}
✅ Completed: Successfully created hello.py file that prints 'Hello, world!' and confirmed it runs correctly.
```

## 💡 Tips

- Start with simple, clear goals
- The agent learns from failures - let it iterate
- Check the verbose output to understand its reasoning
- Extend tools based on your specific use cases

## 🤝 Contributing

This is a minimal educational implementation. Feel free to:
- Add more sophisticated tools
- Implement memory/context management
- Add parallel execution capabilities
- Improve error recovery

---

*Built to understand how coding agents really work, from the ground up.*