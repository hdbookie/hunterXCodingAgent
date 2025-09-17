#!/usr/bin/env python3
"""Setup script for the coding agent."""
import subprocess
import sys
import os

def setup_agent():
    """Set up the coding agent environment."""
    print("🚀 Setting up coding agent...")

    # Check if we're in a virtual environment
    if sys.prefix == sys.base_prefix:
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "agent_env"])

        # Provide activation instructions
        if os.name == "nt":  # Windows
            activate_cmd = "agent_env\\Scripts\\activate"
        else:  # Unix/Linux/Mac
            activate_cmd = "source agent_env/bin/activate"

        print(f"Virtual environment created. To activate, run:")
        print(f"  {activate_cmd}")
        print(f"Then install dependencies with:")
        print(f"  pip install -r requirements.txt")
    else:
        print("Virtual environment detected. Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed!")

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️  Don't forget to set your ANTHROPIC_API_KEY:")
        print("  export ANTHROPIC_API_KEY='your_api_key_here'")
    else:
        print("✅ ANTHROPIC_API_KEY is set!")

    print("\n🎯 Your agent is ready! Try running:")
    print("  python3 coding_agent.py")

if __name__ == "__main__":
    setup_agent()