#!/usr/bin/env python3
"""Interactive runner for the coding agent."""
from coding_agent import run_agent

def main():
    print("🤖 Coding Agent - Interactive Mode")
    print("=" * 40)

    while True:
        print("\nWhat would you like me to build?")
        print("(Type 'quit' to exit)")

        goal = input("\n🎯 Goal: ").strip()

        if goal.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break

        if not goal:
            print("Please enter a goal!")
            continue

        print(f"\n🚀 Starting agent with goal: {goal}")
        print("=" * 60)

        try:
            result = run_agent(goal, max_steps=15, verbose=True)
            print(f"\n✅ Agent completed: {result}")
        except KeyboardInterrupt:
            print("\n⏹️ Agent stopped by user")
        except Exception as e:
            print(f"\n❌ Agent failed: {e}")

        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()