# Mobile Surf Agent - Complete Integration Guide

## Overview

The Mobile Surf Agent is a fully integrated autonomous coding agent that combines Supabase database operations with Railway deployment capabilities to create, deploy, and manage surf instruction mobile applications.

## 🌊 Key Features

- **🗄️ Supabase Integration**: Full database schema management, migrations, and security monitoring
- **🚄 Railway Integration**: Complete deployment pipeline from code to production
- **🤖 Autonomous Development**: AI-powered code generation and deployment
- **📱 Mobile-First**: Optimized for surf instruction app development
- **🔒 Security-First**: Built-in security advisors and best practices
- **📊 Progress Tracking**: PRD compliance monitoring and progress dashboards

## 🚀 Quick Start

### Prerequisites

```bash
# 1. Install FastMCP
pip install fastmcp

# 2. Set up environment variables
export SUPABASE_PROJECT_REF="your_project_ref"
export SUPABASE_ACCESS_TOKEN="your_supabase_token"
export RAILWAY_API_TOKEN="your_railway_token"
```

### Basic Usage

```python
from mobile_surf_agent import MobileSurfAgent

# Initialize the agent
agent = MobileSurfAgent(
    work_directory="./my_surf_app",
    model="qwen2.5-coder:7b",
    verbose=True
)

# Create complete surf app
agent.create_complete_surf_app(
    app_name="SurfMaster Pro",
    features=["session_booking", "progress_tracking", "instructor_ratings"]
)

# Deploy to production
agent.deploy_full_surf_stack(
    railway_project_id="your_railway_project",
    frontend_repo="https://github.com/user/surf-app",
    supabase_url="https://your-project.supabase.co",
    supabase_key="your_anon_key"
)
```

## 🗄️ Supabase Operations

### Database Management

```python
# List all database tables
tables = agent.list_database_tables()

# Set up surf-specific database schema
agent.setup_surf_database()

# Execute custom SQL migrations
agent.execute_sql_migration(
    name="add_user_preferences",
    query="ALTER TABLE users ADD COLUMN surf_level VARCHAR(20);"
)

# Generate TypeScript types
types = agent.generate_database_types()
```

### Security & Monitoring

```python
# Check security advisors
security_report = agent.check_security_advisors()

# Get project configuration
project_url = agent.get_supabase_project_url()
anon_key = agent.get_supabase_anon_key()
```

## 🚄 Railway Deployment

### Project & Service Management

```python
# List Railway projects
projects = agent.list_railway_projects()

# List services in a project
services = agent.list_railway_services(project_id="your_project_id")

# Create new service from GitHub repo
agent.deploy_surf_app_to_railway(
    project_id="your_project_id",
    repo_url="https://github.com/user/surf-frontend",
    service_name="surf-frontend"
)

# Create service from Docker image
agent.create_railway_service_from_image(
    project_id="your_project_id",
    image="nginx:alpine",
    service_name="surf-static"
)
```

### Environment & Configuration

```python
# Configure environment variables
agent.configure_railway_environment(
    project_id="your_project_id",
    service_id="your_service_id",
    env_vars={
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_ANON_KEY": "your_anon_key",
        "NODE_ENV": "production"
    }
)

# Set up custom domain
agent.create_railway_domain(
    project_id="your_project_id",
    service_id="your_service_id",
    domain="surfmaster.app"
)
```

### Deployment & Monitoring

```python
# Trigger new deployment
deployment = agent.trigger_railway_deployment(
    project_id="your_project_id",
    service_id="your_service_id"
)

# Monitor deployment logs
logs = agent.get_railway_deployment_logs(
    deployment_id="deployment_id"
)
```

## 🏗️ Complete Stack Deployment

The agent provides a one-command full-stack deployment that sets up everything needed for a production surf instruction app:

```python
result = agent.deploy_full_surf_stack(
    railway_project_id="11c8154e-1108-4822-8279-710b6eccc454",
    frontend_repo="https://github.com/user/surf-instructor-app",
    supabase_url="https://uhjyhjfmtgcfvfnfqmmt.supabase.co",
    supabase_key="your_anon_key"
)
```

This command:
1. ✅ Sets up Supabase database schema
2. ✅ Deploys frontend to Railway
3. ✅ Configures environment variables
4. ✅ Sets up custom domain
5. ✅ Configures SSL/TLS
6. ✅ Runs security checks
7. ✅ Provides production URLs

## 📊 Progress Tracking

Monitor development progress against your PRD:

```python
from prd_progress_tracker import PRDProgressTracker

# Load your PRD
tracker = PRDProgressTracker("surf_app_prd.yaml")

# Mark progress
tracker.mark_entity_progress("user", "model", True)
tracker.mark_workflow_progress("book_session", "browse_sessions", True)
tracker.mark_deployment_progress("database", True)

# Generate dashboard
dashboard = tracker.generate_progress_dashboard()
print(dashboard)
```

## 🛠️ Available Tools

The agent provides 52 integrated tools across multiple categories:

### Supabase Tools (6)
- `list_database_tables` - List all database tables
- `setup_surf_database` - Set up surf app schema
- `execute_sql_migration` - Execute custom SQL
- `generate_database_types` - Generate TypeScript types
- `get_supabase_project_url` - Get project URL
- `check_security_advisors` - Security monitoring

### Railway Tools (9)
- `list_railway_projects` - List all projects
- `list_railway_services` - List project services
- `deploy_surf_app_to_railway` - Deploy from GitHub
- `create_railway_service_from_image` - Deploy from Docker
- `configure_railway_environment` - Set environment variables
- `create_railway_domain` - Configure custom domains
- `trigger_railway_deployment` - Trigger deployments
- `get_railway_deployment_logs` - Monitor deployments
- `deploy_full_surf_stack` - Complete stack deployment

### Development Tools (37)
- File operations, code generation, testing, and more

## 🔧 Configuration

### Environment Variables

```bash
# Required for Supabase operations
export SUPABASE_PROJECT_REF="uhjyhjfmtgcfvfnfqmmt"
export SUPABASE_ACCESS_TOKEN="your_supabase_access_token"

# Required for Railway operations
export RAILWAY_API_TOKEN="your_railway_api_token"

# Optional: Model configuration
export OLLAMA_MODEL="qwen2.5-coder:7b"
```

### MCP Server Configuration

The agent automatically manages MCP server connections:

```bash
# Supabase MCP Server (auto-managed)
npx -y @supabase/mcp-server-supabase@latest \
  --read-only \
  --project-ref=$SUPABASE_PROJECT_REF \
  --access-token=$SUPABASE_ACCESS_TOKEN

# Railway MCP Server (auto-managed)
npx -y railway-mcp@latest
```

## 🧪 Testing

Run the complete integration test suite:

```bash
# Test complete integration
python test_complete_integration.py

# Test Supabase integration
python test_fastmcp_agent.py

# Test Railway integration
python test_railway_mcp.py
```

## 🎯 Example Workflow

Complete surf instruction app development workflow:

```python
# 1. Initialize agent
agent = MobileSurfAgent(work_directory="./surf_master_app")

# 2. Set up database
agent.setup_surf_database()

# 3. Create app structure
agent.create_complete_surf_app(
    app_name="Surf Master",
    features=[
        "user_authentication",
        "session_booking",
        "progress_tracking",
        "instructor_profiles",
        "weather_integration"
    ]
)

# 4. Deploy to production
agent.deploy_full_surf_stack(
    railway_project_id="your_project_id",
    frontend_repo="https://github.com/user/surf-master",
    supabase_url="https://your-project.supabase.co",
    supabase_key="your_anon_key"
)

# 5. Monitor deployment
logs = agent.get_railway_deployment_logs("deployment_id")
security = agent.check_security_advisors()
```

## 🚨 Error Handling

The agent provides comprehensive error handling:

```python
try:
    result = agent.deploy_full_surf_stack(...)
    if "❌" in result:
        print(f"Deployment failed: {result}")
    else:
        print(f"Deployment successful: {result}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🔐 Security Best Practices

- **Environment Variables**: Never hardcode API tokens
- **Access Tokens**: Use read-only tokens when possible
- **SSL/TLS**: All deployments include HTTPS by default
- **Security Monitoring**: Regular advisor checks
- **Error Handling**: Comprehensive logging and error reporting

## 📚 API Reference

### MobileSurfAgent Class

```python
class MobileSurfAgent:
    def __init__(
        self,
        work_directory: str = "./surf_app",
        model: str = "qwen2.5-coder:7b",
        verbose: bool = False
    )
```

Key methods:
- `create_complete_surf_app()` - Generate complete application
- `setup_surf_database()` - Initialize database schema
- `deploy_full_surf_stack()` - Deploy to production
- `list_database_tables()` - Database operations
- `list_railway_projects()` - Railway operations

## 🤝 Contributing

The Mobile Surf Agent is designed for extensibility:

1. **Add new MCP integrations** in the `_init_surf_tools()` method
2. **Extend database schemas** in `setup_surf_database()`
3. **Add deployment providers** following the Railway pattern
4. **Enhance testing** in the test suite files

## 📞 Support

For issues or questions:
- Check the test files for usage examples
- Review error messages for troubleshooting
- Ensure all environment variables are set correctly
- Verify MCP server connectivity

---

**Ready to build your surf instruction empire? 🏄‍♂️ The Mobile Surf Agent makes it easy!**