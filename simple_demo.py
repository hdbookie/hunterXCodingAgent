#!/usr/bin/env python3
"""Simple demo showing the agent creating hello.py"""
from coding_agent import run_agent

def main():
    goal = "Create a file hello.py that prints 'Hello, world!' and then run it."

    print("🤖 Coding Agent Demo")
    print("=" * 40)
    print(f"Goal: {goal}")
    print("\n" + "=" * 60)

    result = run_agent(goal, max_steps=10, verbose=True)
    print(f"\n✅ Final Result: {result}")

if __name__ == "__main__":
    main()