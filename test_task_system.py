#!/usr/bin/env python3
"""Test the task management system with a complex goal."""
from coding_agent import run_agent

def main():
    print("🧪 Testing Task Management System")
    print("=" * 50)

    # Complex goal that should benefit from task management
    goal = """Create a simple web scraper that:
1. Scrapes quotes from a website
2. Saves the data to a JSON file
3. Creates a summary report
4. Tests the functionality
Use the task system to break this down into manageable steps."""

    print(f"🎯 Complex Goal: {goal}")
    print("\n" + "=" * 60)

    try:
        result = run_agent(goal, max_steps=25, verbose=True)
        print(f"\n✅ Final Result: {result}")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    main()