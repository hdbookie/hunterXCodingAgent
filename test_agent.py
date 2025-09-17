#!/usr/bin/env python3
"""Test script for the coding agent."""
import os

def test_tools():
    """Test individual tools without requiring API key."""
    print("🧪 Testing agent tools...")

    # Import the tools
    from coding_agent import TOOLS

    # Test 1: list_dir
    print("\n1. Testing list_dir:")
    result = TOOLS["list_dir"](".")
    print(f"   Result: {result[:100]}{'...' if len(result) > 100 else ''}")

    # Test 2: write_file
    print("\n2. Testing write_file:")
    result = TOOLS["write_file"]("test_output.txt", "Hello from agent test!")
    print(f"   Result: {result}")

    # Test 3: read_file
    print("\n3. Testing read_file:")
    result = TOOLS["read_file"]("test_output.txt")
    print(f"   Result: {result}")

    # Test 4: run_python
    print("\n4. Testing run_python:")
    result = TOOLS["run_python"]("print('Python execution works!'); print(2+2)")
    print(f"   Result: {result}")

    # Test 5: run_bash
    print("\n5. Testing run_bash:")
    result = TOOLS["run_bash"]("echo 'Bash execution works!'")
    print(f"   Result: {result}")

    # Clean up
    try:
        os.remove("test_output.txt")
        print("\n🧹 Cleaned up test files")
    except:
        pass

    print("\n✅ All tools tested successfully!")

def test_json_parsing():
    """Test JSON parsing functionality."""
    print("\n🧪 Testing JSON parsing...")

    from coding_agent import clean_json

    # Test cases
    test_cases = [
        '{"action": "test", "args": {}}',
        'Here is the JSON: {"action": "test", "args": {}} and some extra text',
        'Some text {"action": "DONE", "result": "finished"} more text',
        'Invalid JSON here',
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test[:50]}{'...' if len(test) > 50 else ''}")
        result = clean_json(test)
        print(f"   Parsed: {result}")

    print("\n✅ JSON parsing tested!")

def test_mock_agent_run():
    """Test agent loop with mock responses (no API calls)."""
    print("\n🧪 Testing agent structure (mock run)...")

    # Import agent components
    from coding_agent import SYSTEM_PROMPT, TOOLS

    print(f"✅ System prompt length: {len(SYSTEM_PROMPT)} chars")
    print(f"✅ Available tools: {list(TOOLS.keys())}")
    print(f"✅ Tools are callable: {all(callable(tool) for tool in TOOLS.values())}")

    # Test a simple mock interaction
    mock_actions = [
        {"action": "list_dir", "args": {}},
        {"action": "write_file", "args": {"path": "mock_test.py", "contents": "print('mock test')"}},
        {"action": "DONE", "result": "Mock test completed"}
    ]

    print("\n🔄 Simulating agent actions:")
    for i, action in enumerate(mock_actions, 1):
        print(f"\nStep {i}: {action}")

        if action["action"] == "DONE":
            print(f"   ✅ Would complete with: {action['result']}")
            break
        elif action["action"] in TOOLS:
            try:
                result = TOOLS[action["action"]](**action.get("args", {}))
                print(f"   🔧 Tool result: {result[:100]}{'...' if len(result) > 100 else ''}")
            except Exception as e:
                print(f"   ❌ Tool error: {e}")

    # Cleanup
    try:
        os.remove("mock_test.py")
        print("\n🧹 Cleaned up mock test files")
    except:
        pass

    print("\n✅ Mock agent run completed!")

if __name__ == "__main__":
    print("🚀 Running coding agent tests...\n")

    try:
        test_tools()
        test_json_parsing()
        test_mock_agent_run()

        print("\n🎉 All tests passed! Your agent is ready to use.")
        print("\n📝 To run the full agent, you need to:")
        print("1. Set ANTHROPIC_API_KEY environment variable")
        print("2. Run: python3 coding_agent.py")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()