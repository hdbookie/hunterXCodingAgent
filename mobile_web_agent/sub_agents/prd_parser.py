"""PRD parsing utilities for extracting development requirements."""

from typing import List


class PRDParser:
    """Parses PRD content to extract development requirements."""

    @staticmethod
    def extract_entities(prd_content: str) -> List[str]:
        """Extract database entities from PRD."""
        entities = []
        lines = prd_content.split('\n')
        in_database_section = False

        for line in lines:
            if "database schema" in line.lower() or "### users table" in line.lower():
                in_database_section = True
            elif line.startswith('##') and in_database_section:
                in_database_section = False
            elif in_database_section and "### " in line and "table" in line.lower():
                entity = line.replace("###", "").replace("Table", "").strip()
                entities.append(entity)

        return entities

    @staticmethod
    def extract_components(prd_content: str) -> List[str]:
        """Extract UI components from PRD."""
        components = []
        lines = prd_content.split('\n')

        for line in lines:
            if "**" in line and any(keyword in line.lower() for keyword in ["component", "card", "form", "list", "dashboard", "builder"]):
                # Extract component name between ** markers
                parts = line.split("**")
                if len(parts) >= 2:
                    component = parts[1].split(":")[0].strip()
                    components.append(component)

        return components

    @staticmethod
    def extract_workflows(prd_content: str) -> List[str]:
        """Extract user workflows from PRD."""
        workflows = []
        lines = prd_content.split('\n')

        for line in lines:
            if "flow:" in line.lower() or "journey" in line.lower():
                workflow = line.replace("###", "").replace(":", "").strip()
                workflows.append(workflow)

        return workflows

    @staticmethod
    def extract_api_endpoints(prd_content: str) -> List[str]:
        """Extract API endpoints from PRD."""
        endpoints = []
        lines = prd_content.split('\n')

        for line in lines:
            if "`/api/" in line:
                # Extract endpoint pattern
                start = line.find("`") + 1
                end = line.find("`", start)
                if end > start:
                    endpoint = line[start:end]
                    endpoints.append(endpoint)

        return endpoints

    @staticmethod
    def extract_database_schema(prd_content: str) -> str:
        """Extract database schema section from PRD."""
        lines = prd_content.split('\n')
        in_schema = False
        schema_lines = []

        for line in lines:
            if "database schema" in line.lower():
                in_schema = True
            elif line.startswith('##') and in_schema and "database" not in line.lower():
                break
            elif in_schema:
                schema_lines.append(line)

        return '\n'.join(schema_lines)

    @staticmethod
    def extract_component_specs(prd_content: str) -> str:
        """Extract component specifications from PRD."""
        lines = prd_content.split('\n')
        in_components = False
        component_lines = []

        for line in lines:
            if "ui component" in line.lower():
                in_components = True
            elif line.startswith('##') and in_components and "component" not in line.lower():
                break
            elif in_components:
                component_lines.append(line)

        return '\n'.join(component_lines)

    @staticmethod
    def extract_workflow_specs(prd_content: str) -> str:
        """Extract workflow specifications from PRD."""
        lines = prd_content.split('\n')
        workflow_lines = []

        for line in lines:
            if "flow:" in line.lower() or "journey" in line.lower():
                workflow_lines.append(line)

        return '\n'.join(workflow_lines)

    @staticmethod
    def extract_api_specs(prd_content: str) -> str:
        """Extract API specifications from PRD."""
        lines = prd_content.split('\n')
        in_api = False
        api_lines = []

        for line in lines:
            if "api endpoint" in line.lower():
                in_api = True
            elif line.startswith('##') and in_api and "api" not in line.lower():
                break
            elif in_api:
                api_lines.append(line)

        return '\n'.join(api_lines)