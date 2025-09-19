"""Sub-agent coordination system."""

from typing import Dict, List, Any, TYPE_CHECKING
from .prd_parser import PRDParser
from .specialist_factory import SpecialistFactory

if TYPE_CHECKING:
    from ..core.agent import MobileWebAgent


class SubAgentCoordinator:
    """Coordinates sub-agent delegation and integration."""

    def __init__(self, main_agent: "MobileWebAgent"):
        self.main_agent = main_agent
        self.prd_parser = PRDParser()
        self.specialist_factory = SpecialistFactory(main_agent)

    def analyze_prd_and_delegate(self, prd_path: str = "prd.md") -> str:
        """Analyze PRD and create specialized sub-agent tasks."""
        try:
            # Read PRD file
            prd_content = self.main_agent.file_ops.read_file(prd_path)
            if "ERROR" in prd_content:
                return f"Failed to read PRD: {prd_content}"

            # Parse PRD to extract components
            entities = self.prd_parser.extract_entities(prd_content)
            components = self.prd_parser.extract_components(prd_content)
            workflows = self.prd_parser.extract_workflows(prd_content)
            api_endpoints = self.prd_parser.extract_api_endpoints(prd_content)

            # Create focused sub-agent tasks
            sub_tasks = []

            if entities:
                sub_tasks.append({
                    "type": "database_specialist",
                    "task": f"Create database schema with tables: {', '.join(entities)}. Include proper relationships, constraints, and security policies.",
                    "tools": ["read_file", "write_file", "run_bash"],
                    "context": self.prd_parser.extract_database_schema(prd_content)
                })

            if components:
                sub_tasks.append({
                    "type": "frontend_specialist",
                    "task": f"Build React components: {', '.join(components)}. Use TypeScript, Tailwind CSS, and mobile-first responsive design.",
                    "tools": ["create_responsive_component", "setup_tailwind", "create_mobile_layout", "read_file", "write_file", "edit_file"],
                    "context": self.prd_parser.extract_component_specs(prd_content)
                })

            if workflows:
                sub_tasks.append({
                    "type": "workflow_specialist",
                    "task": f"Implement user workflows: {', '.join(workflows)}. Create navigation, routing, and user journey flows.",
                    "tools": ["create_responsive_component", "read_file", "write_file", "edit_file"],
                    "context": self.prd_parser.extract_workflow_specs(prd_content)
                })

            if api_endpoints:
                sub_tasks.append({
                    "type": "api_specialist",
                    "task": f"Create API endpoints: {', '.join(api_endpoints)}. Implement CRUD operations with proper validation and error handling.",
                    "tools": ["read_file", "write_file", "edit_file", "run_bash"],
                    "context": self.prd_parser.extract_api_specs(prd_content)
                })

            # Always add testing specialist
            sub_tasks.append({
                "type": "testing_specialist",
                "task": "Create comprehensive test suite with Jest unit tests, Playwright E2E tests, and mobile performance testing.",
                "tools": ["setup_jest", "setup_playwright", "create_unit_tests", "create_e2e_tests", "run_all_tests", "read_file", "write_file"],
                "context": "Test all components, workflows, and API endpoints"
            })

            # Deploy sub-agents and collect results
            results = []
            for task_spec in sub_tasks:
                if self.main_agent.verbose:
                    print(f"🚀 Deploying {task_spec['type']} for: {task_spec['task'][:50]}...")

                result = self.create_specialized_sub_agent(
                    task_spec['type'],
                    task_spec['task'],
                    task_spec['tools'],
                    task_spec['context']
                )
                results.append(f"{task_spec['type']}: {result}")

            return f"""
Sub-agent delegation completed:

Tasks Created: {len(sub_tasks)}
- Database: {'✅' if entities else '⏭️'}
- Frontend: {'✅' if components else '⏭️'}
- Workflows: {'✅' if workflows else '⏭️'}
- API: {'✅' if api_endpoints else '⏭️'}
- Testing: ✅

Results:
{chr(10).join(results)}

Ready for integration and deployment.
"""

        except Exception as e:
            return f"ERROR in PRD analysis and delegation: {e}"

    def create_specialized_sub_agent(self, agent_type: str, task_description: str, allowed_tools: List[str], context: str) -> str:
        """Create and run a specialized sub-agent for focused task."""
        try:
            return self.specialist_factory.create_and_run_specialist(
                agent_type, task_description, allowed_tools, context
            )
        except Exception as e:
            return f"ERROR creating {agent_type}: {e}"