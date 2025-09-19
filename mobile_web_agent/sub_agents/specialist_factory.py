"""Factory for creating specialized sub-agents."""

from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.agent import MobileWebAgent


class SpecialistFactory:
    """Creates and manages specialized sub-agents."""

    def __init__(self, main_agent: "MobileWebAgent"):
        self.main_agent = main_agent

    def create_and_run_specialist(self, agent_type: str, task_description: str, allowed_tools: List[str], context: str) -> str:
        """Create and run a specialized sub-agent for focused task."""
        try:
            # Create specialized system prompt
            specialized_prompt = f"""You are a {agent_type} coding specialist focused on this specific task:

TASK: {task_description}

CONTEXT: {context}

CONSTRAINTS:
- Work autonomously to complete the task
- Use only the provided tools
- Create production-ready code
- Follow best practices for your domain
- Return "TASK_COMPLETE: [summary]" when finished

Available tools: {allowed_tools}

Complete this task systematically and report results."""

            # Create sub-agent instance
            from ..core.agent import MobileWebAgent
            sub_agent = MobileWebAgent(
                work_directory=str(self.main_agent.work_dir),
                model=self.main_agent.model,
                verbose=False  # Keep sub-agents quiet
            )

            # Restrict to only allowed tools
            restricted_tools = {}
            for tool_name in allowed_tools:
                if tool_name in self.main_agent.tools:
                    restricted_tools[tool_name] = self.main_agent.tools[tool_name]

            sub_agent.tools = restricted_tools

            # Run focused task with limited steps
            if self.main_agent.verbose:
                print(f"🔧 Running {agent_type} with {len(allowed_tools)} tools...")

            result = self._run_focused_task(sub_agent, task_description, specialized_prompt, max_steps=15)

            return f"Completed: {result[:200]}..."

        except Exception as e:
            return f"ERROR creating {agent_type}: {e}"

    def _run_focused_task(self, sub_agent: "MobileWebAgent", task_description: str, system_prompt: str, max_steps: int = 15) -> str:
        """Run sub-agent with focused task and specialized prompt."""
        try:
            history = []
            initial_prompt = f"{system_prompt}\\n\\nSTART TASK: {task_description}"

            for step in range(max_steps):
                # Build prompt from history
                if step == 0:
                    prompt = initial_prompt
                else:
                    prompt_parts = [system_prompt, f"TASK: {task_description}"]
                    for h in history[-6:]:  # Keep last 6 exchanges
                        if h['role'] == 'assistant':
                            prompt_parts.append(f"ASSISTANT: {h['content']}")
                        elif h['role'] == 'tool':
                            prompt_parts.append(f"TOOL_RESULT: {h['content']}")
                    prompt = "\\n\\n".join(prompt_parts)

                # Get response from Ollama
                raw_resp = sub_agent.ollama.generate(prompt, max_tokens=1000, temperature=0.1)

                # Check for completion
                if "TASK_COMPLETE:" in raw_resp:
                    return raw_resp.replace("TASK_COMPLETE:", "").strip()

                # Parse and execute action
                action = sub_agent.clean_json(raw_resp)

                if not isinstance(action, dict) or "action" not in action:
                    history.append({"role": "assistant", "content": raw_resp})
                    history.append({"role": "tool", "content": "Response must be valid JSON with 'action' field."})
                    continue

                tool_name = action["action"]
                args = action.get("args", {})

                if tool_name not in sub_agent.tools:
                    error_msg = f"Tool not available: {tool_name}. Available: {list(sub_agent.tools.keys())}"
                    history.append({"role": "assistant", "content": raw_resp})
                    history.append({"role": "tool", "content": error_msg})
                    continue

                # Execute tool
                try:
                    result = sub_agent.tools[tool_name](**args)
                except Exception as e:
                    result = f"Tool execution error: {e}"

                history.append({"role": "assistant", "content": raw_resp})
                history.append({"role": "tool", "content": result})

            return f"Task incomplete after {max_steps} steps"

        except Exception as e:
            return f"ERROR in focused task execution: {e}"