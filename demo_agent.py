#!/usr/bin/env python3
"""Demo version of the coding agent with simulated responses."""
import time
from coding_agent import TOOLS, SYSTEM_PROMPT, clean_json

def simulate_claude_response(step: int, history: list) -> str:
    """Simulate Claude responses for demo purposes."""

    # Simulate thinking time
    time.sleep(1)

    responses = [
        '{"action": "list_dir", "args": {}}',
        '{"action": "write_file", "args": {"path": "hello.py", "contents": "print(\\"Hello, world!\\")\\nprint(\\"This is a test from the coding agent!\\")\\nprint(f\\"2 + 2 = {2 + 2}\\")\\n"}}',
        '{"action": "read_file", "args": {"path": "hello.py"}}',
        '{"action": "run_python", "args": {"code": "exec(open(\\"hello.py\\").read())"}}',
        '{"action": "run_bash", "args": {"cmd": "python3 hello.py"}}',
        '{"action": "DONE", "result": "Successfully created hello.py file with multiple print statements and confirmed it runs correctly. The file prints a greeting, a test message, and a simple calculation."}'
    ]

    if step < len(responses):
        return responses[step]
    else:
        return '{"action": "DONE", "result": "Task completed successfully!"}'

def run_demo_agent(user_goal: str, max_steps: int = 10):
    """Run the coding agent with simulated Claude responses."""

    print(f"🎯 Goal: {user_goal}")
    print("🤖 Running demo with simulated Claude responses...")
    print("=" * 60)

    history = []

    for step in range(max_steps):
        print(f"\n📍 Step {step + 1}")

        # Get simulated response
        raw_resp = simulate_claude_response(step, history)
        print(f"🤖 Claude: {raw_resp}")

        # Parse the action
        action = clean_json(raw_resp)

        if action["action"] == "ERROR":
            print(f"❌ JSON Error: {action.get('args', {}).get('message', 'Unknown error')}")
            continue

        if action["action"] == "DONE":
            result = action.get("result", "Task completed.")
            print(f"✅ Completed: {result}")
            return result

        # Execute the tool
        tool_name = action["action"]
        args = action.get("args", {})

        if tool_name not in TOOLS:
            print(f"❌ Unknown tool: {tool_name}")
            continue

        # Run the tool
        try:
            result = TOOLS[tool_name](**args)
            print(f"🔧 {tool_name}({args}) -> {result[:200]}{'...' if len(result) > 200 else ''}")
        except Exception as e:
            result = f"Tool execution error: {e}"
            print(f"❌ Tool error: {result}")

        history.append({"role": "assistant", "content": raw_resp})
        history.append({"role": "tool", "content": result})

    return f"Demo completed after {max_steps} steps."

if __name__ == "__main__":
    print("🚀 Coding Agent Demo")
    print("This demo simulates Claude responses to show how the agent works.\n")

    goal = "Create a hello.py file that prints multiple messages and then run it to verify it works."

    result = run_demo_agent(goal)

    print(f"\n🎉 Demo Result: {result}")
    print("\n💡 This was a simulation. To use the real agent:")
    print("1. Get an Anthropic API key from https://console.anthropic.com/")
    print("2. Set: export ANTHROPIC_API_KEY='your_key_here'")
    print("3. Run: python3 coding_agent.py")

    # Show the created file
    try:
        with open("hello.py", "r") as f:
            content = f.read()
        print(f"\n📄 Created file content:")
        print("=" * 30)
        print(content)
        print("=" * 30)
    except:
        print("\n📄 No file was created in this demo run")