"""Main Mobile Web Agent orchestrator."""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from ..integrations.ollama_client import OllamaClient
from .file_operations import FileOperations
from .task_manager import TaskManager
from .reflection import ReflectionSystem
from .code_critic import CodeCritic
from ..sub_agents.coordinator import SubAgentCoordinator
from ..tools.mobile_tools import MobileTools
from ..tools.testing_tools import TestingTools


class MobileWebAgent:
    """Main orchestrator for autonomous mobile web development."""

    def __init__(self, work_directory: str = ".", model: str = "qwen2.5-coder:7b", verbose: bool = True):
        self.work_dir = Path(work_directory).resolve()
        self.model = model
        self.verbose = verbose

        # Initialize core systems
        self.ollama = OllamaClient()
        self.ollama.set_model(model)

        self.file_ops = FileOperations(self.work_dir)
        self.task_manager = TaskManager()
        self.code_critic = CodeCritic()
        self.reflection = ReflectionSystem(self.file_ops, self.task_manager, code_critic=self.code_critic)

        # Initialize tools
        self.mobile_tools = MobileTools(self.file_ops)
        self.testing_tools = TestingTools(self.file_ops)

        # Initialize sub-agent coordinator
        self.sub_agent_coordinator = SubAgentCoordinator(self)

        # Build unified tools registry
        self.tools = self._build_tools_registry()

    def _build_tools_registry(self) -> Dict[str, callable]:
        """Build unified registry of all available tools."""
        return {
            # Core file operations
            "read_file": self.file_ops.read_file,
            "write_file": self.file_ops.write_file,
            "edit_file": self.file_ops.edit_file,
            "list_dir": self.file_ops.list_dir,
            "run_bash": self.file_ops.run_bash,
            "grep_search": self.file_ops.grep_search,

            # Task management
            "create_task": self.task_manager.create_task,
            "list_tasks": self.task_manager.list_tasks,
            "complete_task": self.task_manager.complete_task,
            "update_task": self.task_manager.update_task,

            # Reflection
            "reflect_and_assess": self.reflection.reflect_and_assess,
            "assess_code_quality": self.reflection.assess_code_quality,

            # Code quality
            "create_code_critic": self._create_code_critic_sub_agent,
            "critique_code": self._critique_code_wrapper,
            "improve_code_iteratively": self._improve_code_iteratively,

            # Sub-agent coordination
            "analyze_prd_and_delegate": self.sub_agent_coordinator.analyze_prd_and_delegate,
            "create_specialized_sub_agent": self.sub_agent_coordinator.create_specialized_sub_agent,

            # Mobile tools
            "create_pwa_manifest": self.mobile_tools.create_pwa_manifest,
            "create_service_worker": self.mobile_tools.create_service_worker,
            "create_responsive_component": self.mobile_tools.create_responsive_component,
            "setup_tailwind": self.mobile_tools.setup_tailwind,
            "create_mobile_layout": self.mobile_tools.create_mobile_layout,
            "test_mobile_responsive": self.mobile_tools.test_mobile_responsive,

            # Testing tools
            "setup_jest": self.testing_tools.setup_jest,
            "setup_playwright": self.testing_tools.setup_playwright,
            "create_unit_tests": self.testing_tools.create_unit_tests,
            "create_integration_tests": self.testing_tools.create_integration_tests,
            "create_e2e_tests": self.testing_tools.create_e2e_tests,
            "run_all_tests": self.testing_tools.run_all_tests,
            "test_mobile_performance": self.testing_tools.test_mobile_performance,
        }

    def get_system_prompt(self) -> str:
        """Get the system prompt for the mobile web agent."""
        return """You are an autonomous PRD-driven coding agent specialized in mobile web applications. Your approach:

CORE PRINCIPLES:
1. PRD-DRIVEN: All decisions driven by Product Requirements Document
2. PROGRESS-TRACKING: Continuously track implementation against PRD
3. MOBILE-FIRST: Design for mobile, enhance for desktop
4. TESTING-FIRST: Set up comprehensive testing before features
5. DEPLOYMENT-READY: Build for production from day one

CRITICAL WORKFLOW:
1. ALWAYS load PRD first: {"action": "load_prd", "args": {"prd_path": "path/to/prd.md"}}
2. For complex projects, use sub-agent delegation: {"action": "analyze_prd_and_delegate"}
3. Alternative: Generate tasks from PRD: {"action": "create_prd_tasks"}
4. Implement systematically, marking progress after each completion
5. Use progress dashboard to track overall completion
6. Validate implementation against PRD requirements

SUB-AGENT COORDINATION:
- Use analyze_prd_and_delegate() for complex multi-component projects
- Automatically creates specialized agents: database, frontend, testing, API
- Each sub-agent works with focused tools and specific PRD context
- Main agent coordinates integration and final deployment
- Parallel development significantly faster than sequential

Available tools:
=== CORE TOOLS ===
- read_file(path) - Read file contents
- write_file(path, contents) - Write/overwrite files
- edit_file(path, line_range, new_text) - Edit specific lines
- list_dir(path) - List directory contents
- run_bash(cmd) - Run bash commands (allowlisted)
- grep_search(pattern, path) - Search for patterns

=== TASK MANAGEMENT ===
- create_task(description, priority) - Create new task
- list_tasks() - Show all tasks with status
- complete_task(task_id) - Mark task completed
- update_task(task_id, status) - Update task status
- reflect_and_assess(focus) - Reflect on progress and assess current state
- analyze_prd_and_delegate(prd_path) - Parse PRD and deploy specialized sub-agents
- create_specialized_sub_agent(type, task, tools, context) - Create focused specialist

=== MOBILE WEB TOOLS ===
- create_pwa_manifest(app_name, description) - PWA setup
- create_service_worker() - Offline capability
- create_responsive_component(name, props) - Mobile components
- setup_tailwind() - CSS framework
- create_mobile_layout(name) - Mobile-first layouts
- test_mobile_responsive() - Lighthouse mobile testing

=== TESTING TOOLS ===
- setup_jest() - Unit testing framework
- setup_playwright() - E2E testing
- create_unit_tests(component) - Component tests
- create_integration_tests() - Integration tests
- create_e2e_tests() - Full user flow tests
- run_all_tests() - Execute all test suites
- test_mobile_performance() - Performance testing

REFLECTION & QUALITY ASSURANCE:
The agent automatically reflects at key milestones:
- Every 10 steps (safety checkpoint)
- After PRD progress updates
- After testing or deployment actions
- When manually triggered: reflect_and_assess()

Use reflection to:
- Assess progress against PRD goals
- Identify blocking issues or patterns
- Plan course corrections
- Ensure quality and completeness

RESPONSE FORMAT: Always respond with valid JSON only:
{"action": "tool_name", "args": {"param": "value"}}
or
{"action": "DONE", "result": "description of completion"}

Start by understanding the current directory state, create tasks for the goal, then work systematically through implementation with comprehensive testing."""

    def clean_json(self, raw: str) -> Dict[str, Any]:
        """Clean and parse JSON response from Ollama."""
        try:
            # Find first { and last }
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start == -1 or end == 0:
                raise ValueError("No JSON found")

            json_str = raw[start:end]
            return json.loads(json_str)
        except Exception as e:
            if self.verbose:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {raw}")
            return {"action": "ERROR", "args": {"message": f"Failed to parse JSON: {e}"}}

    def run_agent(self, user_goal: str, max_steps: int = 30) -> str:
        """Run the autonomous mobile web agent."""
        if self.verbose:
            print(f"🏄 Mobile Web Agent Goal: {user_goal}")
            print(f"📁 Working Directory: {self.work_dir}")
            print("=" * 50)

        # Check Ollama connection
        if not self.ollama.health_check():
            return "ERROR: Ollama server not running. Please start with 'ollama serve'"

        history = []
        system_prompt = self.get_system_prompt()
        initial_prompt = f"{system_prompt}\\n\\nUSER GOAL: {user_goal}\\n\\nStart by understanding the current directory state, then create tasks to break down this goal."

        for step in range(max_steps):
            if self.verbose:
                print(f"\\n🔄 Step {step + 1}")

            # Build prompt from history
            if step == 0:
                prompt = initial_prompt
            else:
                prompt_parts = [system_prompt, f"GOAL: {user_goal}"]
                for h in history:
                    if h['role'] == 'assistant':
                        prompt_parts.append(f"ASSISTANT: {h['content']}")
                    elif h['role'] == 'tool':
                        prompt_parts.append(f"TOOL_RESULT: {h['content']}")
                prompt = "\\n\\n".join(prompt_parts)

            # Get response from Ollama
            raw_resp = self.ollama.generate(prompt, max_tokens=1500, temperature=0.1)
            if self.verbose:
                print(f"🤖 Response: {raw_resp}")

            # Parse action
            action = self.clean_json(raw_resp)

            if not isinstance(action, dict) or "action" not in action:
                if self.verbose:
                    print(f"❌ Invalid response format: {raw_resp}")
                history.append({"role": "assistant", "content": raw_resp})
                history.append({"role": "tool", "content": "Response must be valid JSON with 'action' field."})
                continue

            if action["action"] == "ERROR":
                if self.verbose:
                    print(f"❌ JSON Error: {action.get('args', {}).get('message', 'Unknown error')}")
                history.append({"role": "assistant", "content": raw_resp})
                history.append({"role": "tool", "content": "JSON parsing failed. Please provide valid JSON."})
                continue

            if action["action"] == "DONE":
                result = action.get("result", "Task completed.")
                if self.verbose:
                    print(f"✅ Completed: {result}")
                return result

            # Execute tool
            tool_name = action["action"]
            args = action.get("args", {})

            if tool_name not in self.tools:
                error_msg = f"Unknown tool: {tool_name}. Available: {list(self.tools.keys())}"
                if self.verbose:
                    print(f"❌ {error_msg}")
                history.append({"role": "assistant", "content": raw_resp})
                history.append({"role": "tool", "content": error_msg})
                continue

            # Run tool
            try:
                result = self.tools[tool_name](**args)
                if self.verbose:
                    display_result = result[:300] + "..." if len(result) > 300 else result
                    print(f"🔧 {tool_name}({args}) -> {display_result}")
            except Exception as e:
                result = f"Tool execution error: {e}"
                if self.verbose:
                    print(f"❌ Tool error: {result}")

            history.append({"role": "assistant", "content": raw_resp})
            history.append({"role": "tool", "content": result})

            # Reflection triggers (simplified for modular structure)
            should_reflect = False

            # Trigger reflection every 10 steps (safety)
            if (step + 1) % 10 == 0:
                should_reflect = True
                if self.verbose:
                    print(f"🔍 Triggering reflection: 10-step checkpoint")

            # Execute reflection if triggered
            if should_reflect:
                if self.verbose:
                    print(f"🔍 Running reflection and assessment...")

                reflection_result = self.reflection.reflect_and_assess()
                history.append({"role": "tool", "content": f"REFLECTION: {reflection_result}"})

                if self.verbose:
                    print(f"🔍 Reflection complete")

        return f"Max steps ({max_steps}) reached without completion."

    def _create_code_critic_sub_agent(self, focus: str = "general") -> str:
        """Create a specialized code critic sub-agent for iterative improvement."""
        try:
            agent_config = {
                "name": f"code_critic_{focus}",
                "type": "code_quality",
                "focus": focus,
                "tools": ["critique_code", "assess_code_quality", "read_file", "write_file", "edit_file"],
                "prompt": f"""You are a specialized code quality critic focused on {focus}.

Your mission: Analyze code for quality issues and provide actionable improvement suggestions.

ANALYSIS AREAS:
- Style and formatting consistency
- Security vulnerabilities
- Performance optimization opportunities
- Maintainability and readability
- Best practices adherence
- Documentation completeness

WORKFLOW:
1. Read and analyze the target code file
2. Use critique_code() to get detailed assessment
3. Prioritize issues by severity (critical → high → medium → low)
4. Provide specific, actionable suggestions with line numbers
5. If authorized, implement improvements directly
6. Re-analyze to verify improvements

RESPONSE FORMAT:
- Clear severity classification
- Specific line references
- Concrete improvement suggestions
- Implementation priority order

Focus on delivering practical, implementable feedback that improves code quality."""
            }

            # Register the sub-agent
            agent_id = self.sub_agent_coordinator.create_specialized_sub_agent(
                "code_quality", agent_config
            )

            return f"Created code critic sub-agent: {agent_id}"

        except Exception as e:
            return f"Error creating code critic sub-agent: {e}"

    def _critique_code_wrapper(self, file_path: str, focus: str = "overall") -> str:
        """Wrapper for code critique that handles file reading and formatting."""
        try:
            if not self.code_critic:
                return "Code critic not initialized"

            # Read the file
            file_content = self.file_ops.read_file(file_path)
            if file_content.startswith("ERROR"):
                return f"Could not read file: {file_content}"

            # Perform critique
            critique_result = self.code_critic.critique_code(file_content, file_path)

            # Format response for agent consumption
            formatted_result = f"""
CODE CRITIQUE RESULTS FOR: {file_path}
{'=' * 60}

QUALITY SCORE: {critique_result['quality_score']}/100
OVERALL ASSESSMENT: {critique_result['overall_assessment']}

ISSUES BREAKDOWN:
- Total Issues: {critique_result['total_issues']}
- Critical: {critique_result['severity_breakdown']['critical']}
- High: {critique_result['severity_breakdown']['high']}
- Medium: {critique_result['severity_breakdown']['medium']}
- Low: {critique_result['severity_breakdown']['low']}

PRIORITY RECOMMENDATIONS:
"""
            for rec in critique_result['recommendations']:
                formatted_result += f"• {rec}\n"

            if critique_result['issues_by_category']:
                formatted_result += "\nDETAILED ISSUES:\n"
                for category, issues in critique_result['issues_by_category'].items():
                    formatted_result += f"\n{category.upper()}:\n"
                    for issue in issues[:3]:  # Show top 3 issues per category
                        line_info = f" (line {issue['line']})" if issue['line'] else ""
                        formatted_result += f"  [{issue['severity']}]{line_info} {issue['message']}\n"
                        formatted_result += f"  💡 {issue['suggestion']}\n"

            return formatted_result

        except Exception as e:
            return f"Error during code critique: {e}"

    def _improve_code_iteratively(self, file_path: str, max_iterations: int = 3, min_score_threshold: float = 85.0) -> str:
        """Iteratively improve code quality through critique-improve cycles."""
        try:
            if not self.code_critic:
                return "Code critic not initialized - cannot perform iterative improvement"

            improvement_log = []
            current_iteration = 0

            # Initial assessment
            initial_critique = self._critique_code_wrapper(file_path, "overall")
            improvement_log.append(f"ITERATION 0 (Initial Assessment):\n{initial_critique}\n")

            # Get initial score
            file_content = self.file_ops.read_file(file_path)
            if file_content.startswith("ERROR"):
                return f"Could not read file for improvement: {file_content}"

            current_critique = self.code_critic.critique_code(file_content, file_path)
            current_score = current_critique['quality_score']

            improvement_log.append(f"Starting score: {current_score}/100")

            # Iterative improvement loop
            for iteration in range(1, max_iterations + 1):
                if current_score >= min_score_threshold:
                    improvement_log.append(f"✅ Quality threshold ({min_score_threshold}) reached at iteration {iteration-1}")
                    break

                improvement_log.append(f"\n--- ITERATION {iteration} ---")

                # Get critical and high priority issues
                critical_issues = [issue for issues in current_critique['issues_by_category'].values()
                                 for issue in issues if issue['severity'] in ['critical', 'high']]

                if not critical_issues:
                    improvement_log.append("No critical or high priority issues found")
                    break

                # Focus on top 3 most severe issues
                top_issues = sorted(critical_issues,
                                  key=lambda x: {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}[x['severity']],
                                  reverse=True)[:3]

                improvement_log.append(f"Addressing {len(top_issues)} priority issues:")

                # Create improvement plan
                improvement_plan = ""
                for i, issue in enumerate(top_issues, 1):
                    line_info = f" (line {issue['line']})" if issue['line'] else ""
                    improvement_plan += f"{i}. [{issue['severity']}]{line_info} {issue['message']}\n"
                    improvement_plan += f"   Solution: {issue['suggestion']}\n"

                improvement_log.append(improvement_plan)

                # Use LLM to implement improvements
                improvement_prompt = f"""You are a code improvement specialist. Analyze this Python file and implement the specific improvements suggested by the code critic.

FILE: {file_path}

CURRENT ISSUES TO FIX:
{improvement_plan}

CURRENT CODE:
{file_content}

Your task:
1. Implement the suggested improvements
2. Focus on the most critical issues first
3. Maintain existing functionality
4. Follow Python best practices
5. Ensure changes are minimal but effective

Respond with the improved code only, no explanations."""

                try:
                    improved_code = self.ollama.generate(improvement_prompt, max_tokens=2000, temperature=0.1)

                    # Basic validation - ensure it's still Python code
                    if improved_code and "def " in improved_code and "import " in improved_code:
                        # Write improved code
                        write_result = self.file_ops.write_file(file_path, improved_code)

                        if write_result.startswith("ERROR"):
                            improvement_log.append(f"❌ Failed to write improvements: {write_result}")
                            break

                        # Re-assess quality
                        new_critique = self.code_critic.critique_code(improved_code, file_path)
                        new_score = new_critique['quality_score']

                        score_improvement = new_score - current_score
                        improvement_log.append(f"Score: {current_score} → {new_score} ({score_improvement:+.1f})")

                        if new_score > current_score:
                            improvement_log.append("✅ Quality improved")
                            current_score = new_score
                            current_critique = new_critique
                            file_content = improved_code
                        else:
                            improvement_log.append("⚠️  No improvement detected")

                    else:
                        improvement_log.append("❌ Generated code appears invalid, skipping")

                except Exception as e:
                    improvement_log.append(f"❌ Improvement iteration failed: {e}")

            # Final assessment
            final_summary = f"""
🔄 ITERATIVE CODE IMPROVEMENT COMPLETE
{'=' * 50}

File: {file_path}
Iterations: {max_iterations}
Final Score: {current_score}/100
Threshold: {min_score_threshold}/100

IMPROVEMENT LOG:
{''.join(improvement_log)}

FINAL STATUS: {'✅ PASSED' if current_score >= min_score_threshold else '⚠️  NEEDS MORE WORK'}
"""
            return final_summary

        except Exception as e:
            return f"Error during iterative improvement: {e}"