"""Main entry point for the Mobile Web Agent."""

import argparse
from .core.agent import MobileWebAgent


def main():
    """Main entry point for the mobile web agent."""
    parser = argparse.ArgumentParser(description="Mobile Web App Coding Agent")
    parser.add_argument("goal", nargs="?", default="Create a mobile web application from PRD",
                       help="Goal for the agent to accomplish")
    parser.add_argument("--dir", default=".", help="Working directory (default: current)")
    parser.add_argument("--model", default="qwen2.5-coder:7b", help="Ollama model to use")
    parser.add_argument("--steps", type=int, default=30, help="Maximum steps")
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")

    args = parser.parse_args()

    # Create agent
    agent = MobileWebAgent(
        work_directory=args.dir,
        model=args.model,
        verbose=not args.quiet
    )

    # Run agent
    result = agent.run_agent(args.goal, max_steps=args.steps)

    print(f"\\n🎉 Final Result: {result}")


if __name__ == "__main__":
    main()