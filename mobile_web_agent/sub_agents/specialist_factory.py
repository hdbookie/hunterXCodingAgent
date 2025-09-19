"""Factory for creating specialized sub-agents."""

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.agent import MobileWebAgent


class SpecialistFactory:
    """Creates and manages specialized sub-agents."""

    def __init__(self, main_agent: "MobileWebAgent"):
        self.main_agent = main_agent

    def create_and_run_specialist(self, agent_type: str, task_description: str, context: str) -> str:
        """Create and run a specialized sub-agent for focused task."""
        try:
            # Create specialized system prompt with domain focus
            specialized_prompt = self._get_specialist_prompt(agent_type, task_description, context)

            # Create sub-agent instance - FULL COPY with all capabilities
            from ..core.agent import MobileWebAgent
            sub_agent = MobileWebAgent(
                work_directory=str(self.main_agent.work_dir),
                model=self.main_agent.model,
                verbose=False  # Keep sub-agents quiet
            )

            # NO tool restrictions - full agent capabilities!
            # Specialization comes from the prompt, not tool limitations

            # Run focused task with reflection capabilities
            if self.main_agent.verbose:
                print(f"🔧 Running {agent_type} with full toolset and reflection...")

            result = self._run_focused_task(sub_agent, task_description, specialized_prompt, max_steps=25)

            return f"Completed: {result[:200]}..."

        except Exception as e:
            return f"ERROR creating {agent_type}: {e}"

    def _run_focused_task(self, sub_agent: "MobileWebAgent", task_description: str, system_prompt: str, max_steps: int = 25) -> str:
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
                raw_resp = sub_agent.ollama.generate(prompt, max_tokens=1500, temperature=0.1)

                # Trigger reflection every 8 steps for quality assurance
                if (step + 1) % 8 == 0:
                    reflection_result = sub_agent.reflection.reflect_and_assess(focus="code_quality")
                    history.append({"role": "tool", "content": f"REFLECTION: {reflection_result}"})

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
                    error_msg = f"Tool not available: {tool_name}. Available: {list(sub_agent.tools.keys())[:10]}..."
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

    def _get_specialist_prompt(self, agent_type: str, task_description: str, context: str) -> str:
        """Generate specialized system prompt for different agent types."""

        base_prompt = f"""You are a {agent_type} specialist with FULL autonomous capabilities. You have access to ALL tools including reflection, quality assessment, and self-improvement.

MISSION: {task_description}

DOMAIN CONTEXT: {context}

SPECIALIZATION GUIDELINES:
"""

        if agent_type == "database_specialist":
            base_prompt += """
- Focus ONLY on database design, schema creation, and data modeling
- Use proper SQL best practices, indexes, constraints, and security
- Implement database migrations and seed data if needed
- Use reflection to validate schema design and performance
- Ensure ACID compliance and proper normalization
"""

        elif agent_type == "frontend_specialist":
            base_prompt += """
- Focus ONLY on React/TypeScript UI components and mobile-first design
- Use Tailwind CSS, responsive design patterns, and accessibility best practices
- Create reusable, well-tested components with proper props interfaces
- Use reflection to assess code quality and mobile optimization
- Follow React best practices: hooks, component composition, performance
"""

        elif agent_type == "workflow_specialist":
            base_prompt += """
- Focus ONLY on user experience flows, navigation, and routing
- Design intuitive user journeys and state management
- Implement proper error handling and loading states
- Use reflection to validate user experience and flow logic
- Consider mobile-first navigation patterns and touch interactions
"""

        elif agent_type == "api_specialist":
            base_prompt += """
- Focus ONLY on backend API development and business logic
- Implement RESTful endpoints with proper validation and error handling
- Use authentication, authorization, and security best practices
- Use reflection to assess API design and performance
- Follow OpenAPI specifications and proper HTTP status codes
"""

        elif agent_type == "testing_specialist":
            base_prompt += """
- Focus ONLY on comprehensive testing strategy and implementation
- Create unit tests, integration tests, and end-to-end tests
- Use Jest, Playwright, and mobile testing frameworks
- Use reflection to assess test coverage and quality
- Implement performance testing and accessibility testing
"""

        base_prompt += f"""

AUTONOMOUS OPERATION:
- Use ALL available tools creatively within your domain
- Reflect on your progress every few steps using reflect_and_assess()
- Use assess_code_quality() to maintain high standards
- Self-correct and iterate when quality is below expectations
- Work systematically but adapt when needed

COMPLETION CRITERIA:
- All domain-specific requirements fully implemented
- Code quality score above 80/100
- Proper testing and validation completed
- Return "TASK_COMPLETE: [detailed summary]" when finished

You are a FULL autonomous agent - use your complete capabilities to deliver excellence in your domain."""

        return base_prompt