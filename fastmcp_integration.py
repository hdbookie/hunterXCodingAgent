"""
FastMCP Integration for Mobile Surf Agent

This module provides direct integration with Supabase and Railway MCP servers using FastMCP client,
replacing the inefficient wrapper pattern with real MCP calls.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from fastmcp import Client
import os


class FastMCPSupabaseClient:
    """FastMCP client for direct Supabase MCP integration."""

    def __init__(self, project_ref: str = None, access_token: str = None):
        self.project_ref = project_ref or os.getenv('SUPABASE_PROJECT_REF', 'uhjyhjfmtgcfvfnfqmmt')
        self.access_token = access_token or os.getenv('SUPABASE_ACCESS_TOKEN')
        self.client = None
        self._initialized = False

    async def initialize(self):
        """Initialize FastMCP client connection to Supabase MCP server."""
        if self._initialized:
            return

        try:
            # Configure the server connection
            server_args = [
                "-y",
                "@supabase/mcp-server-supabase@latest",
                "--read-only",
                f"--project-ref={self.project_ref}"
            ]

            if self.access_token:
                server_args.extend(["--access-token", self.access_token])

            # Configure MCP servers in the correct format
            mcp_config = {
                "mcpServers": {
                    "supabase": {
                        "command": "npx",
                        "args": server_args
                    }
                }
            }

            # Connect to Supabase MCP server with correct configuration
            self.client = Client(transport=mcp_config)
            # Note: Connection will be established when entering async context
            self._initialized = True

        except Exception as e:
            print(f"Failed to initialize FastMCP Supabase client: {e}")
            self._initialized = False

    async def list_tables(self, schemas: List[str] = None) -> Dict[str, Any]:
        """List tables in Supabase database."""
        if not self._initialized:
            await self.initialize()

        try:
            if schemas is None:
                schemas = ["public"]

            async with self.client:
                result = await self.client.call_tool("list_tables", {"schemas": schemas})
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to list tables: {e}"}

    async def execute_sql(self, query: str) -> Dict[str, Any]:
        """Execute SQL query on Supabase database."""
        if not self._initialized:
            await self.initialize()

        try:
            async with self.client:
                result = await self.client.call_tool("execute_sql", {"query": query})
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to execute SQL: {e}"}

    async def apply_migration(self, name: str, query: str) -> Dict[str, Any]:
        """Apply a migration to Supabase database."""
        if not self._initialized:
            await self.initialize()

        try:
            async with self.client:
                result = await self.client.call_tool("apply_migration", {
                    "name": name,
                    "query": query
                })
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to apply migration: {e}"}

    async def get_project_url(self) -> Dict[str, Any]:
        """Get Supabase project API URL."""
        if not self._initialized:
            await self.initialize()

        try:
            async with self.client:
                result = await self.client.call_tool("get_project_url", {})
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to get project URL: {e}"}

    async def get_anon_key(self) -> Dict[str, Any]:
        """Get Supabase anonymous API key."""
        if not self._initialized:
            await self.initialize()

        try:
            async with self.client:
                result = await self.client.call_tool("get_anon_key", {})
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to get anon key: {e}"}

    async def get_advisors(self, advisor_type: str = "security") -> Dict[str, Any]:
        """Get security/performance advisors from Supabase."""
        if not self._initialized:
            await self.initialize()

        try:
            async with self.client:
                result = await self.client.call_tool("get_advisors", {"type": advisor_type})
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to get advisors: {e}"}

    async def deploy_edge_function(self, name: str, files: List[Dict]) -> Dict[str, Any]:
        """Deploy an Edge Function to Supabase."""
        if not self._initialized:
            await self.initialize()

        try:
            async with self.client:
                result = await self.client.call_tool("deploy_edge_function", {
                    "name": name,
                    "files": files
                })
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to deploy edge function: {e}"}

    async def close(self):
        """Close the FastMCP client connection."""
        if self.client and self._initialized:
            await self.client.close()
            self._initialized = False


class FastMCPRailwayClient:
    """FastMCP client for direct Railway MCP integration."""

    def __init__(self, api_token: str = None):
        self.api_token = api_token or os.getenv('RAILWAY_API_TOKEN')
        self.client = None
        self._initialized = False

    async def initialize(self):
        """Initialize FastMCP client connection to Railway MCP server."""
        if self._initialized:
            return

        try:
            # Configure the server connection using railway-mcp package
            server_args = [
                "-y",
                "railway-mcp@latest"
            ]

            # Configure MCP servers in the correct format
            mcp_config = {
                "mcpServers": {
                    "railway": {
                        "command": "npx",
                        "args": server_args,
                        "env": {
                            "RAILWAY_API_TOKEN": self.api_token
                        } if self.api_token else {}
                    }
                }
            }

            # Connect to Railway MCP server with correct configuration
            self.client = Client(transport=mcp_config)
            # Note: Connection will be established when entering async context
            self._initialized = True

        except Exception as e:
            print(f"Failed to initialize FastMCP Railway client: {e}")
            self._initialized = False

    async def project_list(self) -> Dict[str, Any]:
        """List Railway projects."""
        if not self._initialized:
            await self.initialize()

        try:
            async with self.client:
                result = await self.client.call_tool("project_list", {})
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to list projects: {e}"}

    async def service_list(self, project_id: str) -> Dict[str, Any]:
        """List services in a Railway project."""
        if not self._initialized:
            await self.initialize()

        try:
            async with self.client:
                result = await self.client.call_tool("service_list", {"projectId": project_id})
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to list services: {e}"}

    async def service_create_from_repo(self, project_id: str, repo: str, name: str = None) -> Dict[str, Any]:
        """Create a service from a GitHub repository."""
        if not self._initialized:
            await self.initialize()

        try:
            params = {"projectId": project_id, "repo": repo}
            if name:
                params["name"] = name

            async with self.client:
                result = await self.client.call_tool("service_create_from_repo", params)
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to create service from repo: {e}"}

    async def variable_set(self, project_id: str, environment_id: str, name: str, value: str, service_id: str = None) -> Dict[str, Any]:
        """Set environment variable."""
        if not self._initialized:
            await self.initialize()

        try:
            params = {
                "projectId": project_id,
                "environmentId": environment_id,
                "name": name,
                "value": value
            }
            if service_id:
                params["serviceId"] = service_id

            async with self.client:
                result = await self.client.call_tool("variable_set", params)
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to set variable: {e}"}

    async def domain_create(self, environment_id: str, service_id: str, domain: str = None) -> Dict[str, Any]:
        """Create a domain for a service."""
        if not self._initialized:
            await self.initialize()

        try:
            params = {
                "environmentId": environment_id,
                "serviceId": service_id
            }
            if domain:
                params["domain"] = domain

            async with self.client:
                result = await self.client.call_tool("domain_create", params)
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to create domain: {e}"}

    async def deployment_trigger(self, project_id: str, service_id: str, environment_id: str) -> Dict[str, Any]:
        """Trigger a deployment."""
        if not self._initialized:
            await self.initialize()

        try:
            async with self.client:
                result = await self.client.call_tool("deployment_trigger", {
                    "projectId": project_id,
                    "serviceId": service_id,
                    "environmentId": environment_id
                })
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to trigger deployment: {e}"}

    async def configure_api_token(self, token: str) -> Dict[str, Any]:
        """Configure Railway API token using the configure tool."""
        if not self._initialized:
            await self.initialize()

        try:
            async with self.client:
                result = await self.client.call_tool("configure_api_token", {"token": token})
                return result.content[0].text if hasattr(result, 'content') and result.content else result
        except Exception as e:
            return {"error": f"Failed to configure API token: {e}"}

    async def close(self):
        """Close the FastMCP client connection."""
        if self.client and self._initialized:
            await self.client.close()
            self._initialized = False


class AsyncMCPSupabaseAdapter:
    """Synchronous adapter for async FastMCP Supabase operations."""

    def __init__(self, project_ref: str = None, access_token: str = None):
        self.client = FastMCPSupabaseClient(project_ref, access_token)
        self.loop = None

    def _run_async(self, coro):
        """Run async operation in sync context."""
        try:
            # Try to get existing event loop
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            # Create new event loop if none exists
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        if self.loop.is_running():
            # If loop is already running, use asyncio.run_coroutine_threadsafe
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        else:
            # Run in the current loop
            return self.loop.run_until_complete(coro)

    def list_tables(self, schemas: List[str] = None) -> str:
        """List tables (sync wrapper)."""
        result = self._run_async(self.client.list_tables(schemas))
        return json.dumps(result)

    def execute_sql(self, query: str) -> str:
        """Execute SQL (sync wrapper)."""
        result = self._run_async(self.client.execute_sql(query))
        return json.dumps(result)

    def apply_migration(self, name: str, query: str) -> str:
        """Apply migration (sync wrapper)."""
        result = self._run_async(self.client.apply_migration(name, query))
        return json.dumps(result)

    def get_project_url(self) -> str:
        """Get project URL (sync wrapper)."""
        result = self._run_async(self.client.get_project_url())
        return json.dumps(result)

    def get_anon_key(self) -> str:
        """Get anon key (sync wrapper)."""
        result = self._run_async(self.client.get_anon_key())
        return json.dumps(result)

    def get_advisors(self, advisor_type: str = "security") -> str:
        """Get advisors (sync wrapper)."""
        result = self._run_async(self.client.get_advisors(advisor_type))
        return json.dumps(result)

    def deploy_edge_function(self, name: str, files: List[Dict]) -> str:
        """Deploy edge function (sync wrapper)."""
        result = self._run_async(self.client.deploy_edge_function(name, files))
        return json.dumps(result)

    def create_surf_app_database(self) -> str:
        """Create database schema for surf instruction app."""
        schema_sql = """
        -- Users table (teachers and students)
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            role TEXT CHECK (role IN ('teacher', 'student')) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Surf sessions table
        CREATE TABLE IF NOT EXISTS surf_sessions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            teacher_id UUID REFERENCES users(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            description TEXT,
            location TEXT,
            session_date TIMESTAMP WITH TIME ZONE NOT NULL,
            duration_minutes INTEGER DEFAULT 60,
            max_students INTEGER DEFAULT 8,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Student enrollments
        CREATE TABLE IF NOT EXISTS enrollments (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            student_id UUID REFERENCES users(id) ON DELETE CASCADE,
            session_id UUID REFERENCES surf_sessions(id) ON DELETE CASCADE,
            enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            attendance_status TEXT CHECK (attendance_status IN ('enrolled', 'attended', 'missed')) DEFAULT 'enrolled',
            notes TEXT,
            UNIQUE(student_id, session_id)
        );

        -- Student progress tracking
        CREATE TABLE IF NOT EXISTS student_progress (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            student_id UUID REFERENCES users(id) ON DELETE CASCADE,
            skill_category TEXT NOT NULL,
            skill_level INTEGER CHECK (skill_level BETWEEN 1 AND 10) DEFAULT 1,
            notes TEXT,
            assessed_by UUID REFERENCES users(id),
            assessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Row Level Security policies
        ALTER TABLE users ENABLE ROW LEVEL SECURITY;
        ALTER TABLE surf_sessions ENABLE ROW LEVEL SECURITY;
        ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;
        ALTER TABLE student_progress ENABLE ROW LEVEL SECURITY;
        """

        return self.apply_migration("create_surf_app_schema", schema_sql)

    def close(self):
        """Close connections."""
        if self.client:
            self._run_async(self.client.close())


class AsyncMCPRailwayAdapter:
    """Synchronous adapter for async FastMCP Railway operations."""

    def __init__(self, api_token: str = None):
        self.client = FastMCPRailwayClient(api_token)
        self.loop = None

    def _run_async(self, coro):
        """Run async operation in sync context."""
        try:
            # Try to get existing event loop
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            # Create new event loop if none exists
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        if self.loop.is_running():
            # If loop is already running, use asyncio.run_coroutine_threadsafe
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        else:
            # Run in the current loop
            return self.loop.run_until_complete(coro)

    def project_list(self) -> str:
        """List Railway projects (sync wrapper)."""
        result = self._run_async(self.client.project_list())
        return json.dumps(result)

    def service_list(self, project_id: str) -> str:
        """List services in a Railway project (sync wrapper)."""
        result = self._run_async(self.client.service_list(project_id))
        return json.dumps(result)

    def service_create_from_repo(self, project_id: str, repo: str, name: str = None) -> str:
        """Create a service from a GitHub repository (sync wrapper)."""
        result = self._run_async(self.client.service_create_from_repo(project_id, repo, name))
        return json.dumps(result)

    def variable_set(self, project_id: str, environment_id: str, name: str, value: str, service_id: str = None) -> str:
        """Set environment variable (sync wrapper)."""
        result = self._run_async(self.client.variable_set(project_id, environment_id, name, value, service_id))
        return json.dumps(result)

    def domain_create(self, environment_id: str, service_id: str, domain: str = None) -> str:
        """Create a domain for a service (sync wrapper)."""
        result = self._run_async(self.client.domain_create(environment_id, service_id, domain))
        return json.dumps(result)

    def deployment_trigger(self, project_id: str, service_id: str, environment_id: str) -> str:
        """Trigger a deployment (sync wrapper)."""
        result = self._run_async(self.client.deployment_trigger(project_id, service_id, environment_id))
        return json.dumps(result)

    def configure_api_token(self, token: str) -> str:
        """Configure Railway API token (sync wrapper)."""
        result = self._run_async(self.client.configure_api_token(token))
        return json.dumps(result)

    def close(self):
        """Close connections."""
        if self.client:
            self._run_async(self.client.close())


# Test function
def test_fastmcp_integration():
    """Test FastMCP Supabase integration."""
    print("🧪 Testing FastMCP Supabase Integration...")

    try:
        adapter = AsyncMCPSupabaseAdapter()

        # Test basic connection and table listing
        print("📋 Testing table listing...")
        tables_result = adapter.list_tables()
        print(f"Tables result: {tables_result}")

        # Test project URL retrieval
        print("🔗 Testing project URL...")
        url_result = adapter.get_project_url()
        print(f"URL result: {url_result}")

        # Close connections
        adapter.close()

        print("✅ FastMCP integration test completed")

    except Exception as e:
        print(f"❌ FastMCP integration test failed: {e}")


if __name__ == "__main__":
    test_fastmcp_integration()