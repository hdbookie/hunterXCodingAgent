#!/usr/bin/env python3
"""
Mobile Surf App Coding Agent

An autonomous coding agent specialized for building mobile-first surf instruction web apps.
Features:
- Local Ollama LLM (zero cost)
- Directory-aware operation (Claude Code style)
- Supabase & Railway MCP integration
- Testing-first development approach
- Mobile web app specialization
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import our local modules
from ollama_client import OllamaClient, create_ollama_call
from fastmcp_integration import AsyncMCPSupabaseAdapter, AsyncMCPRailwayAdapter
from real_mcp_bridge import RealMCPBridge, SurfAppMCPTasks
from prd_progress_tracker import PRDProgressTracker

class MobileSurfAgent:
    """Autonomous coding agent for mobile surf instruction apps."""

    def __init__(self, work_directory: str = ".", model: str = "qwen2.5-coder:7b", verbose: bool = True):
        self.work_dir = Path(work_directory).resolve()
        self.model = model
        self.verbose = verbose

        # Initialize components
        self.ollama = OllamaClient()
        self.ollama.set_model(model)
        self.supabase_mcp = AsyncMCPSupabaseAdapter()
        self.railway_mcp = AsyncMCPRailwayAdapter()
        self.mcp_bridge = RealMCPBridge()
        self.surf_mcp_tasks = SurfAppMCPTasks()
        self.prd_tracker = PRDProgressTracker()

        # Task management (inherit from original agent)
        self.tasks = []
        self.task_counter = 0

        # Mobile web app specific tools
        self.mobile_tools = self._init_mobile_tools()
        self.surf_tools = self._init_surf_tools()
        self.testing_tools = self._init_testing_tools()

        # Combined tools registry
        self.tools = {
            **self._init_core_tools(),
            **self.mobile_tools,
            **self.surf_tools,
            **self.testing_tools,
            **self._init_prd_tools()
        }

    def _init_core_tools(self) -> Dict[str, callable]:
        """Initialize core file/system tools (inherited from original agent)."""
        return {
            "read_file": self.read_file,
            "write_file": self.write_file,
            "edit_file": self.edit_file,
            "list_dir": self.list_dir,
            "run_bash": self.run_bash,
            "grep_search": self.grep_search,
            "create_task": self.create_task,
            "list_tasks": self.list_tasks,
            "complete_task": self.complete_task,
            "update_task": self.update_task,
            "reflect_and_assess": self.reflect_and_assess,
            "analyze_prd_and_delegate": self.analyze_prd_and_delegate,
            "create_specialized_sub_agent": self.create_specialized_sub_agent
        }

    def _init_mobile_tools(self) -> Dict[str, callable]:
        """Initialize mobile web development tools."""
        return {
            "create_pwa_manifest": self.create_pwa_manifest,
            "create_service_worker": self.create_service_worker,
            "create_responsive_component": self.create_responsive_component,
            "setup_tailwind": self.setup_tailwind,
            "create_mobile_layout": self.create_mobile_layout,
            "test_mobile_responsive": self.test_mobile_responsive
        }

    def _init_surf_tools(self) -> Dict[str, callable]:
        """Initialize infrastructure and deployment tools."""
        return {
            # Supabase database tools
            "setup_database_schema": self.setup_database_schema,
            "list_database_tables": self.list_database_tables,
            "execute_database_query": self.execute_database_query,
            "apply_database_migration": self.apply_database_migration,
            "get_supabase_project_url": self.get_supabase_project_url,
            "get_supabase_anon_key": self.get_supabase_anon_key,
            "check_security_advisors": self.check_security_advisors,

            # Railway deployment tools
            "list_railway_projects": self.list_railway_projects,
            "list_railway_services": self.list_railway_services,
            "deploy_surf_app_to_railway": self.deploy_surf_app_to_railway,
            "create_railway_service_from_image": self.create_railway_service_from_image,
            "configure_railway_environment": self.configure_railway_environment,
            "create_railway_domain": self.create_railway_domain,
            "trigger_railway_deployment": self.trigger_railway_deployment,
            "get_railway_deployment_logs": self.get_railway_deployment_logs,
            "configure_railway_api_token": self.configure_railway_api_token,
            "deploy_full_surf_stack": self.deploy_full_surf_stack,

            # General tools
            "execute_real_mcp_call": self.execute_real_mcp_call,
            "get_deployment_workflow": self.get_deployment_workflow
        }

    def _init_testing_tools(self) -> Dict[str, callable]:
        """Initialize comprehensive testing tools."""
        return {
            "setup_jest": self.setup_jest,
            "setup_playwright": self.setup_playwright,
            "create_unit_tests": self.create_unit_tests,
            "create_integration_tests": self.create_integration_tests,
            "create_e2e_tests": self.create_e2e_tests,
            "run_all_tests": self.run_all_tests,
            "test_mobile_performance": self.test_mobile_performance
        }

    def _init_prd_tools(self) -> Dict[str, callable]:
        """Initialize PRD-driven development tools."""
        return {
            "load_prd": self.load_prd,
            "create_prd_tasks": self.create_prd_tasks,
            "mark_entity_progress": self.mark_entity_progress,
            "mark_workflow_progress": self.mark_workflow_progress,
            "mark_component_progress": self.mark_component_progress,
            "mark_deployment_progress": self.mark_deployment_progress,
            "generate_progress_dashboard": self.generate_progress_dashboard,
            "get_next_priorities": self.get_next_priorities,
            "validate_against_prd": self.validate_against_prd,
            "export_progress": self.export_progress
        }

    # Core file operations (from original agent)
    def read_file(self, path: str) -> str:
        """Read file contents relative to work directory."""
        try:
            full_path = self.work_dir / path
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"ERROR: {e}"

    def write_file(self, path: str, contents: str) -> str:
        """Write file contents relative to work directory."""
        try:
            full_path = self.work_dir / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(contents)
            return f"Successfully wrote {len(contents)} characters to {path}"
        except Exception as e:
            return f"ERROR: {e}"

    def edit_file(self, path: str, line_range: str, new_text: str) -> str:
        """Edit specific lines in a file."""
        try:
            full_path = self.work_dir / path
            with open(full_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if ":" in line_range:
                start, end = map(int, line_range.split(":"))
            else:
                start = end = int(line_range)

            start_idx = max(0, start - 1)
            end_idx = min(len(lines), end)

            lines[start_idx:end_idx] = [new_text + "\n" if not new_text.endswith("\n") else new_text]

            with open(full_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return f"Successfully edited lines {start}:{end} in {path}"
        except Exception as e:
            return f"ERROR: {e}"

    def list_dir(self, path: str = ".") -> str:
        """List directory contents relative to work directory."""
        try:
            full_path = self.work_dir / path
            items = sorted(full_path.iterdir())
            result = []
            for item in items:
                if item.is_dir():
                    result.append(f"[DIR]  {item.name}")
                else:
                    result.append(f"[FILE] {item.name}")
            return "\n".join(result)
        except Exception as e:
            return f"ERROR: {e}"

    def run_bash(self, cmd: str, cwd: str = ".") -> str:
        """Run bash command in work directory with safety restrictions."""
        # Enhanced allowlist for mobile development
        allowed = [
            "npm", "yarn", "pnpm", "node", "python3", "python", "pip",
            "git", "ls", "echo", "cat", "grep", "pwd", "which", "wc", "head", "tail",
            "find", "tree", "jest", "playwright", "cypress", "lighthouse",
            "mkdir", "touch", "rm", "cp", "mv", "chmod"
        ]

        if not any(cmd.startswith(a) for a in allowed):
            return f"ERROR: Command not allowed: {cmd}. Allowed: {', '.join(allowed)}"

        try:
            full_cwd = self.work_dir / cwd
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=full_cwd,
                capture_output=True,
                text=True,
                timeout=60
            )
            output = ""
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}"
            if result.returncode != 0:
                output += f"Return code: {result.returncode}"
            return output or "Command completed with no output"
        except subprocess.TimeoutExpired:
            return "ERROR: Command timed out after 60 seconds"
        except Exception as e:
            return f"ERROR: {e}"

    def grep_search(self, pattern: str, path: str = ".") -> str:
        """Search for patterns in files."""
        try:
            full_path = self.work_dir / path
            result = subprocess.run(
                ["grep", "-rnI", "--include=*.py", "--include=*.js", "--include=*.ts",
                 "--include=*.tsx", "--include=*.jsx", "--include=*.html", "--include=*.css", pattern, str(full_path)],
                capture_output=True,
                text=True,
                timeout=15
            )
            return result.stdout if result.stdout else "No matches found"
        except Exception as e:
            return f"ERROR: {e}"

    # Task management (from original agent)
    def create_task(self, description: str, priority: str = "medium") -> str:
        """Create a new task with description and priority."""
        self.task_counter += 1
        task = {
            "id": self.task_counter,
            "description": description,
            "status": "pending",
            "priority": priority
        }
        self.tasks.append(task)
        return f"Created task #{self.task_counter}: {description}"

    def list_tasks(self) -> str:
        """List all tasks with their current status."""
        if not self.tasks:
            return "No tasks created yet"

        result = "Current Tasks:\n" + "=" * 40 + "\n"
        for task in self.tasks:
            status_icon = {
                "pending": "☐",
                "in_progress": "🔄",
                "completed": "✅"
            }.get(task["status"], "❓")
            result += f"{status_icon} #{task['id']}: {task['description']} [{task['status']}]\n"

        pending = len([t for t in self.tasks if t["status"] == "pending"])
        in_progress = len([t for t in self.tasks if t["status"] == "in_progress"])
        completed = len([t for t in self.tasks if t["status"] == "completed"])

        result += f"\nSummary: {pending} pending, {in_progress} in progress, {completed} completed"
        return result

    def complete_task(self, task_id: str) -> str:
        """Mark a task as completed."""
        try:
            task_id_int = int(task_id)
            for task in self.tasks:
                if task["id"] == task_id_int:
                    task["status"] = "completed"
                    return f"✅ Completed task #{task_id}: {task['description']}"
            return f"ERROR: Task #{task_id} not found"
        except ValueError:
            return f"ERROR: Invalid task ID '{task_id}'. Use a number."

    def update_task(self, task_id: str, status: str) -> str:
        """Update task status."""
        valid_statuses = ["pending", "in_progress", "completed"]
        if status not in valid_statuses:
            return f"ERROR: Invalid status '{status}'. Use: {', '.join(valid_statuses)}"

        try:
            task_id_int = int(task_id)
            for task in self.tasks:
                if task["id"] == task_id_int:
                    old_status = task["status"]
                    task["status"] = status
                    return f"Updated task #{task_id} from '{old_status}' to '{status}'"
            return f"ERROR: Task #{task_id} not found"
        except ValueError:
            return f"ERROR: Invalid task ID '{task_id}'. Use a number."

    def reflect_and_assess(self, focus: str = "overall") -> str:
        """Reflect on recent progress and assess current state."""
        try:
            # Get current state
            task_summary = self.list_tasks()

            if self.prd_tracker.prd:
                progress_dashboard = self.prd_tracker.generate_progress_dashboard()
                next_priorities = self.prd_tracker.get_next_priorities()
            else:
                progress_dashboard = "No PRD loaded"
                next_priorities = []

            # Analyze current directory structure
            current_files = self.list_dir(".")

            reflection = f"""
🔍 REFLECTION AND ASSESSMENT
{'=' * 40}

CURRENT TASK STATUS:
{task_summary}

PRD PROGRESS:
{progress_dashboard}

CURRENT PROJECT STATE:
{current_files}

NEXT PRIORITIES:
"""
            for i, priority in enumerate(next_priorities[:5], 1):
                reflection += f"{i}. {priority}\n"

            reflection += f"""
ASSESSMENT QUESTIONS:
- Are we making progress toward PRD goals? {"Yes" if self.prd_tracker.prd else "No PRD loaded"}
- Are there any blocking issues in recent actions?
- Do we have proper project structure in place?
- Are tests set up and passing?
- Is the current approach working effectively?

RECOMMENDATIONS:
"""

            # Basic heuristics for recommendations
            if "No PRD loaded" in progress_dashboard:
                reflection += "- CRITICAL: Load PRD file first to guide development\n"

            if "package.json" not in current_files and "No files found" not in current_files:
                reflection += "- Consider setting up project structure (package.json, src/, etc.)\n"

            pending_tasks = len([t for t in self.tasks if t["status"] == "pending"])
            in_progress_tasks = len([t for t in self.tasks if t["status"] == "in_progress"])

            if in_progress_tasks > 1:
                reflection += "- Focus: Complete current in-progress tasks before starting new ones\n"
            elif pending_tasks == 0 and in_progress_tasks == 0:
                reflection += "- Create specific tasks based on PRD requirements\n"

            reflection += "\nREFLECTION COMPLETE - Ready to continue development."

            return reflection

        except Exception as e:
            return f"ERROR during reflection: {e}"

    # Sub-Agent Coordination System
    def analyze_prd_and_delegate(self, prd_path: str = "prd.md") -> str:
        """Analyze PRD and create specialized sub-agent tasks."""
        try:
            # Read PRD file
            prd_content = self.read_file(prd_path)
            if "ERROR" in prd_content:
                return f"Failed to read PRD: {prd_content}"

            # Parse PRD to extract components
            entities = self._extract_entities(prd_content)
            components = self._extract_components(prd_content)
            workflows = self._extract_workflows(prd_content)
            api_endpoints = self._extract_api_endpoints(prd_content)

            # Create focused sub-agent tasks
            sub_tasks = []

            if entities:
                sub_tasks.append({
                    "type": "database_specialist",
                    "task": f"Create Supabase database schema with tables: {', '.join(entities)}. Include proper relationships, constraints, and Row Level Security policies.",
                    "tools": ["setup_database_schema", "execute_database_query", "apply_database_migration", "read_file", "write_file"],
                    "context": self._extract_database_schema(prd_content)
                })

            if components:
                sub_tasks.append({
                    "type": "frontend_specialist",
                    "task": f"Build React components: {', '.join(components)}. Use TypeScript, Tailwind CSS, and mobile-first responsive design.",
                    "tools": ["create_responsive_component", "setup_tailwind", "create_mobile_layout", "read_file", "write_file", "edit_file"],
                    "context": self._extract_component_specs(prd_content)
                })

            if workflows:
                sub_tasks.append({
                    "type": "workflow_specialist",
                    "task": f"Implement user workflows: {', '.join(workflows)}. Create navigation, routing, and user journey flows.",
                    "tools": ["create_responsive_component", "read_file", "write_file", "edit_file"],
                    "context": self._extract_workflow_specs(prd_content)
                })

            if api_endpoints:
                sub_tasks.append({
                    "type": "api_specialist",
                    "task": f"Create API endpoints: {', '.join(api_endpoints)}. Implement CRUD operations with proper validation and error handling.",
                    "tools": ["read_file", "write_file", "edit_file", "run_bash"],
                    "context": self._extract_api_specs(prd_content)
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
                if self.verbose:
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

    def create_specialized_sub_agent(self, agent_type: str, task_description: str, allowed_tools: list, context: str) -> str:
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
            sub_agent = MobileSurfAgent(
                work_directory=self.work_dir,
                model=self.model,
                verbose=False  # Keep sub-agents quiet
            )

            # Restrict to only allowed tools
            restricted_tools = {}
            for tool_name in allowed_tools:
                if tool_name in self.tools:
                    restricted_tools[tool_name] = self.tools[tool_name]

            sub_agent.tools = restricted_tools

            # Run focused task with limited steps
            if self.verbose:
                print(f"🔧 Running {agent_type} with {len(allowed_tools)} tools...")

            result = sub_agent.run_focused_task(task_description, specialized_prompt, max_steps=15)

            return f"Completed: {result[:200]}..."

        except Exception as e:
            return f"ERROR creating {agent_type}: {e}"

    def run_focused_task(self, task_description: str, system_prompt: str, max_steps: int = 15) -> str:
        """Run sub-agent with focused task and specialized prompt."""
        try:
            history = []
            initial_prompt = f"{system_prompt}\n\nSTART TASK: {task_description}"

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
                    prompt = "\n\n".join(prompt_parts)

                # Get response from Ollama
                raw_resp = self.ollama.generate(prompt, max_tokens=1000, temperature=0.1)

                # Check for completion
                if "TASK_COMPLETE:" in raw_resp:
                    return raw_resp.replace("TASK_COMPLETE:", "").strip()

                # Parse and execute action
                action = self.clean_json(raw_resp)

                if not isinstance(action, dict) or "action" not in action:
                    history.append({"role": "assistant", "content": raw_resp})
                    history.append({"role": "tool", "content": "Response must be valid JSON with 'action' field."})
                    continue

                tool_name = action["action"]
                args = action.get("args", {})

                if tool_name not in self.tools:
                    error_msg = f"Tool not available: {tool_name}. Available: {list(self.tools.keys())}"
                    history.append({"role": "assistant", "content": raw_resp})
                    history.append({"role": "tool", "content": error_msg})
                    continue

                # Execute tool
                try:
                    result = self.tools[tool_name](**args)
                except Exception as e:
                    result = f"Tool execution error: {e}"

                history.append({"role": "assistant", "content": raw_resp})
                history.append({"role": "tool", "content": result})

            return f"Task incomplete after {max_steps} steps"

        except Exception as e:
            return f"ERROR in focused task execution: {e}"

    # PRD Parsing Utilities
    def _extract_entities(self, prd_content: str) -> list:
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

    def _extract_components(self, prd_content: str) -> list:
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

    def _extract_workflows(self, prd_content: str) -> list:
        """Extract user workflows from PRD."""
        workflows = []
        lines = prd_content.split('\n')

        for line in lines:
            if "flow:" in line.lower() or "journey" in line.lower():
                workflow = line.replace("###", "").replace(":", "").strip()
                workflows.append(workflow)

        return workflows

    def _extract_api_endpoints(self, prd_content: str) -> list:
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

    def _extract_database_schema(self, prd_content: str) -> str:
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

    def _extract_component_specs(self, prd_content: str) -> str:
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

    def _extract_workflow_specs(self, prd_content: str) -> str:
        """Extract workflow specifications from PRD."""
        lines = prd_content.split('\n')
        workflow_lines = []

        for line in lines:
            if "flow:" in line.lower() or "journey" in line.lower():
                workflow_lines.append(line)

        return '\n'.join(workflow_lines)

    def _extract_api_specs(self, prd_content: str) -> str:
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

    # Mobile web development tools
    def create_pwa_manifest(self, app_name: str, description: str = "Surf Instruction App") -> str:
        """Create PWA manifest.json file."""
        manifest = {
            "name": app_name,
            "short_name": app_name,
            "description": description,
            "start_url": "/",
            "display": "standalone",
            "background_color": "#0ea5e9",
            "theme_color": "#0ea5e9",
            "orientation": "portrait-primary",
            "icons": [
                {
                    "src": "/icon-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "/icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }

        content = json.dumps(manifest, indent=2)
        return self.write_file("public/manifest.json", content)

    def create_service_worker(self) -> str:
        """Create basic service worker for PWA."""
        sw_content = """
// Service Worker for Surf App PWA
const CACHE_NAME = 'surf-app-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
"""
        return self.write_file("public/sw.js", sw_content.strip())

    def create_responsive_component(self, component_name: str, props: str = "") -> str:
        """Create a responsive React component template."""
        component_content = f"""
import React from 'react';

interface {component_name}Props {{
  {props}
}}

const {component_name}: React.FC<{component_name}Props> = (props) => {{
  return (
    <div className="w-full max-w-md mx-auto p-4 sm:max-w-lg md:max-w-xl lg:max-w-2xl">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          {component_name}
        </h2>
        {{/* Component content here */}}
      </div>
    </div>
  );
}};

export default {component_name};
"""
        return self.write_file(f"src/components/{component_name}.tsx", component_content.strip())

    def setup_tailwind(self) -> str:
        """Set up Tailwind CSS for the project."""
        # Tailwind config
        config_content = """
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        'surf-blue': '#0ea5e9',
        'surf-teal': '#14b8a6',
        'surf-sand': '#fbbf24'
      }
    },
  },
  plugins: [],
}
"""
        result1 = self.write_file("tailwind.config.js", config_content.strip())

        # CSS file
        css_content = """
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply font-sans antialiased;
  }
}

@layer components {
  .btn-surf {
    @apply bg-surf-blue hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition-colors;
  }

  .card-surf {
    @apply bg-white rounded-lg shadow-md p-6 border border-gray-200;
  }
}
"""
        result2 = self.write_file("src/index.css", css_content.strip())

        return f"{result1}\n{result2}"

    def create_mobile_layout(self, layout_name: str) -> str:
        """Create mobile-first layout component."""
        layout_content = f"""
import React from 'react';

interface {layout_name}Props {{
  children: React.ReactNode;
  title?: string;
}}

const {layout_name}: React.FC<{layout_name}Props> = ({{ children, title }}) => {{
  return (
    <div className="min-h-screen bg-gray-50">
      {{/* Mobile Header */}}
      <header className="bg-surf-blue text-white p-4 sticky top-0 z-10">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-bold">{{title || 'Surf App'}}</h1>
          <button className="p-2 hover:bg-blue-600 rounded">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={{2}} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </header>

      {{/* Main Content */}}
      <main className="pb-16 sm:pb-0">
        {{children}}
      </main>

      {{/* Mobile Bottom Navigation */}}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 sm:hidden">
        <div className="grid grid-cols-4 py-2">
          <button className="flex flex-col items-center p-2 text-surf-blue">
            <span className="text-xs mt-1">Home</span>
          </button>
          <button className="flex flex-col items-center p-2 text-gray-600">
            <span className="text-xs mt-1">Sessions</span>
          </button>
          <button className="flex flex-col items-center p-2 text-gray-600">
            <span className="text-xs mt-1">Progress</span>
          </button>
          <button className="flex flex-col items-center p-2 text-gray-600">
            <span className="text-xs mt-1">Profile</span>
          </button>
        </div>
      </nav>
    </div>
  );
}};

export default {layout_name};
"""
        return self.write_file(f"src/components/{layout_name}.tsx", layout_content.strip())

    def test_mobile_responsive(self) -> str:
        """Test mobile responsiveness using Lighthouse."""
        return self.run_bash("npx lighthouse --only-categories=performance,accessibility --form-factor=mobile --chrome-flags='--headless' http://localhost:3000")

    # Surf app domain tools

    def setup_database_schema(self) -> str:
        """Set up Supabase database schema using FastMCP integration."""
        try:
            # Use the FastMCP adapter to create the database schema
            result = self.supabase_mcp.create_surf_app_database()

            return f"""
✅ Surf app database schema created successfully!

Result: {result}

Created tables:
- users (teachers and students)
- surf_sessions
- enrollments
- student_progress

With proper Row Level Security enabled.
"""
        except Exception as e:
            return f"❌ Failed to create surf app database: {e}"

    def list_database_tables(self, schemas: List[str] = None) -> str:
        """List tables in Supabase database using FastMCP."""
        try:
            result = self.supabase_mcp.list_tables(schemas)
            return f"✅ Database tables listed successfully:\n{result}"
        except Exception as e:
            return f"❌ Failed to list tables: {e}"

    def execute_database_query(self, query: str) -> str:
        """Execute SQL query on Supabase database using FastMCP."""
        try:
            result = self.supabase_mcp.execute_sql(query)
            return f"✅ SQL query executed successfully:\n{result}"
        except Exception as e:
            return f"❌ Failed to execute query: {e}"

    def apply_database_migration(self, name: str, sql: str) -> str:
        """Apply database migration using FastMCP."""
        try:
            result = self.supabase_mcp.apply_migration(name, sql)
            return f"✅ Migration '{name}' applied successfully:\n{result}"
        except Exception as e:
            return f"❌ Failed to apply migration: {e}"

    def get_supabase_project_url(self) -> str:
        """Get Supabase project API URL using FastMCP."""
        try:
            result = self.supabase_mcp.get_project_url()
            return f"✅ Project URL retrieved:\n{result}"
        except Exception as e:
            return f"❌ Failed to get project URL: {e}"

    def get_supabase_anon_key(self) -> str:
        """Get Supabase anonymous API key using FastMCP."""
        try:
            result = self.supabase_mcp.get_anon_key()
            return f"✅ Anonymous key retrieved:\n{result}"
        except Exception as e:
            return f"❌ Failed to get anon key: {e}"

    def check_security_advisors(self) -> str:
        """Check Supabase security advisors using FastMCP."""
        try:
            result = self.supabase_mcp.get_advisors("security")
            return f"🔒 Security advisors:\n{result}"
        except Exception as e:
            return f"❌ Failed to get security advisors: {e}"

    def execute_real_mcp_call(self, service: str, action: str, **kwargs) -> str:
        """Execute a real MCP call using the bridge."""
        instruction = self.mcp_bridge.get_mcp_call_instruction(service, action, **kwargs)

        if 'error' in instruction:
            return f"MCP Call Error: {instruction['error']}"

        return f"""
Real MCP Call Required:
Tool: {instruction['tool']}
Parameters: {json.dumps(instruction['parameters'], indent=2)}

Instruction: {instruction['instruction']}
"""

    def get_deployment_workflow(self) -> str:
        """Get complete deployment workflow with real MCP calls."""
        from real_mcp_bridge import get_surf_deployment_instructions

        workflow = get_surf_deployment_instructions()

        output = f"""
🌊 SURF APP DEPLOYMENT WORKFLOW ({workflow['total_tasks']} tasks)

Prerequisites:
"""
        for prereq in workflow['prerequisites']:
            output += f"  - {prereq}\n"

        output += "\nDeployment Tasks:\n"
        for i, task in enumerate(workflow['tasks'], 1):
            output += f"\n{i}. {task['description']}\n"
            for step in task['steps']:
                output += f"   → {step['action']}: {step['tool']}\n"

        output += f"\nExecution: {workflow['execution_order']}\n"
        output += f"Rollback: {workflow['rollback_strategy']}\n"

        return output

    # Railway deployment methods
    def list_railway_projects(self) -> str:
        """List Railway projects using FastMCP."""
        try:
            result = self.railway_mcp.project_list()
            return f"✅ Railway projects listed successfully:\n{result}"
        except Exception as e:
            return f"❌ Failed to list Railway projects: {e}"

    def list_railway_services(self, project_id: str) -> str:
        """List services in a Railway project using FastMCP."""
        try:
            result = self.railway_mcp.service_list(project_id)
            return f"✅ Railway services listed successfully:\n{result}"
        except Exception as e:
            return f"❌ Failed to list Railway services: {e}"

    def deploy_surf_app_to_railway(self, project_id: str, repo_url: str, service_name: str = "surf-frontend") -> str:
        """Deploy surf app frontend to Railway using FastMCP."""
        try:
            # Create service from repository
            result = self.railway_mcp.service_create_from_repo(project_id, repo_url, service_name)
            return f"✅ Surf app deployed to Railway successfully:\n{result}"
        except Exception as e:
            return f"❌ Failed to deploy surf app to Railway: {e}"

    def create_railway_service_from_image(self, project_id: str, image: str, service_name: str) -> str:
        """Create Railway service from Docker image using FastMCP."""
        try:
            result = self.railway_mcp.service_create_from_image(project_id, image, service_name)
            return f"✅ Railway service created from image:\n{result}"
        except Exception as e:
            return f"❌ Failed to create Railway service: {e}"

    def configure_railway_environment(self, project_id: str, environment_id: str, service_id: str, variables: dict) -> str:
        """Configure environment variables for Railway service using FastMCP."""
        try:
            result = self.railway_mcp.variable_bulk_set(project_id, environment_id, variables, service_id)
            return f"✅ Railway environment variables configured:\n{result}"
        except Exception as e:
            return f"❌ Failed to configure Railway environment: {e}"

    def create_railway_domain(self, environment_id: str, service_id: str, domain: str = None) -> str:
        """Create domain for Railway service using FastMCP."""
        try:
            result = self.railway_mcp.domain_create(environment_id, service_id, domain)
            return f"✅ Railway domain created:\n{result}"
        except Exception as e:
            return f"❌ Failed to create Railway domain: {e}"

    def trigger_railway_deployment(self, project_id: str, service_id: str, environment_id: str, commit_sha: str) -> str:
        """Trigger Railway deployment using FastMCP."""
        try:
            result = self.railway_mcp.deployment_trigger(project_id, service_id, environment_id, commit_sha)
            return f"✅ Railway deployment triggered:\n{result}"
        except Exception as e:
            return f"❌ Failed to trigger Railway deployment: {e}"

    def get_railway_deployment_logs(self, deployment_id: str) -> str:
        """Get Railway deployment logs using FastMCP."""
        try:
            result = self.railway_mcp.deployment_logs(deployment_id)
            return f"✅ Railway deployment logs:\n{result}"
        except Exception as e:
            return f"❌ Failed to get Railway deployment logs: {e}"

    def configure_railway_api_token(self, token: str) -> str:
        """Configure Railway API token using FastMCP."""
        try:
            result = self.railway_mcp.configure_api_token(token)
            return f"✅ Railway API token configured:\n{result}"
        except Exception as e:
            return f"❌ Failed to configure Railway API token: {e}"

    def deploy_full_surf_stack(self, railway_project_id: str, frontend_repo: str, supabase_url: str, supabase_key: str) -> str:
        """Deploy complete surf instruction app stack (Supabase + Railway)."""
        try:
            # Step 1: Set up Supabase database
            db_result = self.setup_database_schema()

            # Step 2: Deploy frontend to Railway
            deploy_result = self.deploy_surf_app_to_railway(railway_project_id, frontend_repo)

            # Step 3: Configure environment variables
            env_vars = {
                "NEXT_PUBLIC_SUPABASE_URL": supabase_url,
                "NEXT_PUBLIC_SUPABASE_ANON_KEY": supabase_key,
                "NODE_ENV": "production"
            }

            # Get service info to find environment_id and service_id
            services = self.list_railway_services(railway_project_id)

            return f"""
✅ Full surf app stack deployment initiated:

Database Setup:
{db_result}

Frontend Deployment:
{deploy_result}

Services:
{services}

Next steps:
1. Configure environment variables with actual service ID
2. Set up custom domain
3. Test the deployment
"""
        except Exception as e:
            return f"❌ Failed to deploy full surf stack: {e}"

    # Testing tools
    def setup_jest(self) -> str:
        """Set up Jest testing framework."""
        jest_config = """
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapping: {
    '\\\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{js,jsx,ts,tsx}',
    '<rootDir>/src/**/*.{spec,test}.{js,jsx,ts,tsx}'
  ],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.tsx'
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    }
  }
};
"""

        setup_tests = """
import '@testing-library/jest-dom';
"""

        result1 = self.write_file("jest.config.js", jest_config.strip())
        result2 = self.write_file("src/setupTests.ts", setup_tests.strip())

        return f"{result1}\n{result2}"

    def setup_playwright(self) -> str:
        """Set up Playwright for E2E testing."""
        playwright_config = """
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'npm start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
"""
        return self.write_file("playwright.config.ts", playwright_config.strip())

    def create_unit_tests(self, component_name: str) -> str:
        """Create unit tests for a component."""
        test_content = f"""
import React from 'react';
import {{ render, screen, fireEvent }} from '@testing-library/react';
import {component_name} from '../{component_name}';

describe('{component_name}', () => {{
  it('renders without crashing', () => {{
    render(<{component_name} />);
    expect(screen.getByText('{component_name}')).toBeInTheDocument();
  }});

  it('handles user interactions correctly', () => {{
    render(<{component_name} />);
    // Add specific interaction tests here
  }});

  it('displays correct data when props are provided', () => {{
    const testProps = {{
      // Add test props here
    }};
    render(<{component_name} {{...testProps}} />);
    // Add assertions here
  }});
}});
"""
        return self.write_file(f"src/components/__tests__/{component_name}.test.tsx", test_content.strip())

    def create_integration_tests(self) -> str:
        """Create integration tests."""
        test_content = """
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

describe('App Integration Tests', () => {
  it('navigates between pages correctly', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Test navigation flow
    expect(screen.getByText('Surf App')).toBeInTheDocument();

    // Add more integration test scenarios
  });

  it('handles form submissions correctly', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Test form interactions
    // Add form testing logic
  });
});
"""
        return self.write_file("src/__tests__/App.integration.test.tsx", test_content.strip())

    def create_e2e_tests(self) -> str:
        """Create end-to-end tests with Playwright."""
        e2e_content = """
import { test, expect } from '@playwright/test';

test.describe('Surf App E2E Tests', () => {
  test('mobile navigation works correctly', async ({ page }) => {
    await page.goto('/');

    // Test mobile responsive behavior
    await page.setViewportSize({ width: 375, height: 812 });

    await expect(page.getByText('Surf App')).toBeVisible();

    // Test bottom navigation
    await page.getByText('Sessions').click();
    await expect(page).toHaveURL(/.*sessions/);
  });

  test('session scheduling flow', async ({ page }) => {
    await page.goto('/schedule');

    // Fill out session form
    await page.fill('input[placeholder*="Session Title"]', 'Test Session');
    await page.fill('input[type="date"]', '2024-12-25');
    await page.fill('input[type="time"]', '14:00');

    await page.click('button[type="submit"]');

    // Verify session was created
    await expect(page.getByText('Session created successfully')).toBeVisible();
  });

  test('progress tracking updates', async ({ page }) => {
    await page.goto('/progress');

    // Test progress interaction
    await expect(page.getByText('Progress Tracker')).toBeVisible();

    // Check skill levels are displayed
    await expect(page.getByText('Paddle Out')).toBeVisible();
    await expect(page.getByText('Pop Up')).toBeVisible();
  });
});
"""
        return self.write_file("tests/e2e/surf-app.spec.ts", e2e_content.strip())

    def run_all_tests(self) -> str:
        """Run all test suites."""
        results = []

        # Run unit tests
        results.append("=== UNIT TESTS ===")
        results.append(self.run_bash("npm test -- --coverage --watchAll=false"))

        # Run E2E tests
        results.append("\n=== E2E TESTS ===")
        results.append(self.run_bash("npx playwright test"))

        return "\n".join(results)

    def test_mobile_performance(self) -> str:
        """Test mobile performance using Lighthouse."""
        return self.run_bash("npx lighthouse --only-categories=performance --form-factor=mobile --output=json --output-path=./lighthouse-mobile.json http://localhost:3000")

    # PRD-Driven Development Tools
    def load_prd(self, prd_path: str) -> str:
        """Load PRD file and initialize progress tracking."""
        result = self.prd_tracker.load_prd(prd_path)
        return json.dumps(result)

    def create_prd_tasks(self, project_type: str = "mobile_web") -> str:
        """Create task list based on loaded PRD requirements."""
        if not self.prd_tracker.prd:
            return json.dumps({"error": "No PRD loaded. Use load_prd(path) first."})

        # Get next priorities from PRD
        priorities = self.prd_tracker.get_next_priorities()

        # Create tasks for top priorities
        task_results = []
        for priority in priorities[:5]:  # Top 5 priorities
            task_result = self.create_task(priority, "high")
            task_results.append(task_result)

        return json.dumps({
            "created_tasks": len(task_results),
            "priorities": priorities[:5],
            "task_results": task_results
        })

    def mark_entity_progress(self, entity_name: str, aspect: str, completed: bool = True) -> str:
        """Mark progress on entity implementation (model, crud, ui, tests)."""
        result = self.prd_tracker.mark_entity_progress(entity_name, aspect, completed)
        return result

    def mark_workflow_progress(self, workflow_name: str, step: str, completed: bool = True) -> str:
        """Mark progress on workflow step implementation."""
        result = self.prd_tracker.mark_workflow_progress(workflow_name, step, completed)
        return result

    def mark_component_progress(self, component_name: str, aspect: str, completed: bool = True) -> str:
        """Mark progress on component implementation (implemented, tested)."""
        result = self.prd_tracker.mark_component_progress(component_name, aspect, completed)
        return result

    def mark_deployment_progress(self, aspect: str, completed: bool = True) -> str:
        """Mark progress on deployment aspects (database, backend, frontend, domain, ssl)."""
        result = self.prd_tracker.mark_deployment_progress(aspect, completed)
        return result

    def generate_progress_dashboard(self) -> str:
        """Generate comprehensive progress dashboard from PRD."""
        dashboard = self.prd_tracker.generate_progress_dashboard()
        return dashboard

    def get_next_priorities(self) -> str:
        """Get next priority tasks based on PRD and current progress."""
        priorities = self.prd_tracker.get_next_priorities()
        return json.dumps({
            "next_priorities": priorities[:10],
            "total_priorities": len(priorities),
            "overall_progress": self.prd_tracker.get_overall_progress()
        })

    def validate_against_prd(self, project_path: str = ".") -> str:
        """Validate current implementation against PRD requirements."""
        result = self.prd_tracker.validate_against_prd(project_path)
        return json.dumps(result, indent=2)

    def export_progress(self, output_path: str = "prd_progress.json") -> str:
        """Export progress data to JSON file."""
        result = self.prd_tracker.export_progress(output_path)
        return result

    # Agent system prompt for surf app specialization
    def get_system_prompt(self) -> str:
        """Get the system prompt for the mobile surf agent."""
        return """You are an autonomous PRD-driven coding agent specialized in mobile web applications. Your approach:

CORE PRINCIPLES:
1. PRD-DRIVEN: All decisions driven by Product Requirements Document
2. PROGRESS-TRACKING: Continuously track implementation against PRD
3. MOBILE-FIRST: Design for mobile, enhance for desktop
4. TESTING-FIRST: Set up comprehensive testing before features
5. DEPLOYMENT-READY: Build for production from day one

CRITICAL WORKFLOW:
1. ALWAYS load PRD first: {"action": "load_prd", "args": {"prd_path": "path/to/prd.yaml"}}
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

=== PRD-DRIVEN DEVELOPMENT ===
- load_prd(prd_path) - Load and parse PRD file
- create_prd_tasks() - Generate tasks from PRD requirements
- mark_entity_progress(entity, aspect, completed) - Track entity implementation
- mark_workflow_progress(workflow, step, completed) - Track workflow steps
- mark_component_progress(component, aspect, completed) - Track components
- mark_deployment_progress(aspect, completed) - Track deployment
- generate_progress_dashboard() - View comprehensive progress
- get_next_priorities() - Get next tasks based on PRD
- validate_against_prd(project_path) - Check compliance
- export_progress(output_path) - Export progress report

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

=== INFRASTRUCTURE & DEPLOYMENT ===
- setup_database_schema() - Set up database schema
- execute_real_mcp_call(service, action) - Execute MCP calls
- get_deployment_workflow() - Get deployment instructions

PRD PROGRESS TRACKING WORKFLOW:
After implementing any feature/component/entity:
1. Mark appropriate progress: mark_entity_progress("user", "model", true)
2. Check priorities: get_next_priorities()
3. Generate dashboard periodically: generate_progress_dashboard()
4. Validate compliance: validate_against_prd(".")

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
        """Run the autonomous surf agent."""
        if self.verbose:
            print(f"🏄 Mobile Surf Agent Goal: {user_goal}")
            print(f"📁 Working Directory: {self.work_dir}")
            print("=" * 50)

        # Check Ollama connection
        if not self.ollama.health_check():
            return "ERROR: Ollama server not running. Please start with 'ollama serve'"

        history = []
        system_prompt = self.get_system_prompt()
        initial_prompt = f"{system_prompt}\n\nUSER GOAL: {user_goal}\n\nStart by understanding the current directory state, then create tasks to break down this goal."

        for step in range(max_steps):
            if self.verbose:
                print(f"\n🔄 Step {step + 1}")

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
                prompt = "\n\n".join(prompt_parts)

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

            # Reflection triggers
            should_reflect = False

            # Trigger reflection every 10 steps (safety)
            if (step + 1) % 10 == 0:
                should_reflect = True
                if self.verbose:
                    print(f"🔍 Triggering reflection: 10-step checkpoint")

            # Trigger reflection after PRD-related actions
            prd_actions = ["load_prd", "mark_entity_progress", "mark_workflow_progress",
                          "mark_component_progress", "mark_deployment_progress"]
            if tool_name in prd_actions:
                should_reflect = True
                if self.verbose:
                    print(f"🔍 Triggering reflection: PRD action completed")

            # Trigger reflection after testing actions
            test_actions = ["run_all_tests", "setup_jest", "setup_playwright"]
            if tool_name in test_actions:
                should_reflect = True
                if self.verbose:
                    print(f"🔍 Triggering reflection: Testing action completed")

            # Trigger reflection after deployment actions
            deploy_actions = ["deploy_full_surf_stack", "trigger_railway_deployment",
                            "create_railway_domain"]
            if tool_name in deploy_actions:
                should_reflect = True
                if self.verbose:
                    print(f"🔍 Triggering reflection: Deployment action completed")

            # Execute reflection if triggered
            if should_reflect:
                if self.verbose:
                    print(f"🔍 Running reflection and assessment...")

                reflection_result = self.reflect_and_assess()
                history.append({"role": "tool", "content": f"REFLECTION: {reflection_result}"})

                if self.verbose:
                    print(f"🔍 Reflection complete")

        return f"Max steps ({max_steps}) reached without completion."

def main():
    """Main entry point for the mobile surf agent."""
    parser = argparse.ArgumentParser(description="Mobile Surf App Coding Agent")
    parser.add_argument("goal", nargs="?", default="Create a mobile surf instruction web app",
                       help="Goal for the agent to accomplish")
    parser.add_argument("--dir", default=".", help="Working directory (default: current)")
    parser.add_argument("--model", default="qwen2.5-coder:7b", help="Ollama model to use")
    parser.add_argument("--steps", type=int, default=30, help="Maximum steps")
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")

    args = parser.parse_args()

    # Create agent
    agent = MobileSurfAgent(
        work_directory=args.dir,
        model=args.model,
        verbose=not args.quiet
    )

    # Run agent
    result = agent.run_agent(args.goal, max_steps=args.steps)

    print(f"\n🎉 Final Result: {result}")

if __name__ == "__main__":
    main()