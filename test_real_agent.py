#!/usr/bin/env python3
"""Test the real agent with a simple goal."""
from coding_agent import run_agent

if __name__ == "__main__":
    print("🚀 Testing the real coding agent with Claude API...")

    # Simple test goal
    goal = "Create a file called greeting.py that asks for the user's name and prints a personalized greeting, then test it works."

    print(f"🎯 Goal: {goal}")
    print("=" * 60)

    try:
        result = run_agent(goal, max_steps=10, verbose=True)
        print(f"\n🎉 Agent completed with result: {result}")
    except Exception as e:
        print(f"\n❌ Agent failed with error: {e}")
        import traceback
        traceback.print_exc()