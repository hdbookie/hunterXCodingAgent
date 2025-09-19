# 🚀 Autonomous Mobile Web Agent

A sophisticated autonomous coding agent specialized in mobile web development with **sub-agent architecture**, **reflection capabilities**, and **code quality assessment**. This system can build complete mobile web applications from Product Requirements Documents (PRDs) with minimal human intervention.

## 🌟 **Key Features**

### 🧠 **Autonomous Multi-Agent System**
- **Main Coordinator**: Orchestrates complex projects and delegates to specialists
- **Sub-Agent Specialists**: Database, Frontend, API, Workflow, and Testing experts
- **Full Tool Access**: Each sub-agent has complete autonomous capabilities (no artificial restrictions)
- **Domain Focus**: Specialization through intelligent prompts, not tool limitations

### 🔍 **Advanced Reflection & Quality**
- **Self-Assessment**: Continuous reflection on progress and code quality
- **Code Critique**: Automated code quality scoring and improvement suggestions
- **Iterative Improvement**: Agents can self-correct and enhance their output
- **Quality Gates**: 80+ code quality score requirements for completion

### 📱 **Mobile-First Development**
- **PWA Support**: Progressive Web App manifests and service workers
- **Responsive Components**: Mobile-first React/TypeScript components
- **Tailwind Integration**: Modern CSS framework setup
- **Performance Testing**: Lighthouse mobile optimization

### 🛠 **Comprehensive Toolset**
- **File Operations**: Read, write, edit with smart context awareness
- **Mobile Tools**: PWA creation, responsive layouts, mobile testing
- **Testing Framework**: Jest, Playwright, E2E, and performance testing
- **Database Tools**: Schema design, migrations, security best practices
- **Code Quality**: Assessment, critique, and iterative improvement

## 🎯 **How It Works**

### 1. **PRD-Driven Development**
```
PRD Analysis → Component Extraction → Sub-Agent Delegation → Integration → Deployment
```

### 2. **Sub-Agent Architecture**
```python
# Each specialist is a FULL autonomous agent with complete toolset
Database Specialist    → Schema design, migrations, security
Frontend Specialist    → React components, mobile-first UI
API Specialist        → RESTful endpoints, authentication
Workflow Specialist    → User journeys, navigation, routing
Testing Specialist     → Comprehensive test suites
```

### 3. **Reflection Loop**
```
Code Creation → Quality Assessment → Self-Critique → Improvement → Validation
```

## 🚀 **Quick Start**

### Prerequisites
- **Python 3.8+**
- **Ollama** with `qwen2.5-coder:7b` model
- **Node.js** (for mobile web development)

### Installation

1. **Start Ollama**:
   ```bash
   ollama serve
   ollama pull qwen2.5-coder:7b
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Your PRD**:
   ```markdown
   # My Mobile App PRD

   ## Database Schema
   ### Users Table
   - id, email, password_hash

   ## UI Components
   **UserCard**: Display user profile
   **Dashboard**: Main app interface

   ## API Endpoints
   `/api/users` - User management
   ```

4. **Run the Agent**:
   ```bash
   python -m mobile_web_agent.main "Build mobile app from prd.md"
   ```

## 📋 **Command Line Options**

```bash
python -m mobile_web_agent.main [goal] [options]

Options:
  --dir DIR          Working directory (default: current)
  --model MODEL      Ollama model (default: qwen2.5-coder:7b)
  --steps STEPS      Maximum steps (default: 30)
  --quiet           Reduce output verbosity
```

## 🏗 **Architecture Deep Dive**

### Core Components

#### **Main Agent** (`core/agent.py`)
- **30 tools** including reflection, quality assessment, mobile development
- **Sub-agent coordination** with intelligent delegation
- **Progress tracking** and task management
- **Error recovery** and adaptation

#### **Sub-Agent Coordinator** (`sub_agents/coordinator.py`)
- **PRD parsing** to extract entities, components, workflows
- **Specialist creation** with domain-focused prompts
- **Parallel execution** for faster development
- **Result integration** and deployment coordination

#### **Reflection System** (`core/reflection.py`)
- **Progress assessment** against PRD goals
- **Code quality analysis** with detailed scoring
- **Blocking issue detection** and course correction
- **Project structure validation**

#### **Specialist Factory** (`sub_agents/specialist_factory.py`)
- **Full agent cloning** (complete toolset, no restrictions)
- **Domain-specific prompts** for focused expertise
- **Quality triggers** every 8 steps for assessment
- **25-step execution** with reflection and improvement

### Tool Categories

#### **Core Operations**
```python
read_file, write_file, edit_file, list_dir, run_bash, grep_search
```

#### **Task Management**
```python
create_task, list_tasks, complete_task, update_task
```

#### **Reflection & Quality**
```python
reflect_and_assess, assess_code_quality, critique_code, improve_code_iteratively
```

#### **Mobile Development**
```python
create_pwa_manifest, create_service_worker, create_responsive_component,
setup_tailwind, create_mobile_layout, test_mobile_responsive
```

#### **Testing**
```python
setup_jest, setup_playwright, create_unit_tests, create_e2e_tests,
run_all_tests, test_mobile_performance
```

## 🎨 **Example Workflow**

### Input PRD:
```markdown
# Todo Mobile App

## Database Schema
### Users Table: id, email, password_hash
### Todos Table: id, user_id, title, completed

## UI Components
**TodoCard**: Individual todo display
**TodoList**: Todo container with filtering

## API Endpoints
`/api/todos` - CRUD operations
`/api/auth/login` - Authentication
```

### Autonomous Execution:
```
🔍 PRD Analysis
├── 📊 Database entities: [Users, Todos]
├── 🎨 Components: [TodoCard, TodoList]
└── 🌐 Endpoints: [/api/todos, /api/auth/login]

🚀 Sub-Agent Deployment
├── 🗄️  Database Specialist → Schema + migrations
├── ⚛️  Frontend Specialist → React components
├── 🌐 API Specialist → Express endpoints
└── 🧪 Testing Specialist → Comprehensive tests

🔄 Reflection & Quality
├── 📈 Code quality: 85/100
├── 🔍 Mobile optimization: ✅
└── 🎯 PRD completion: 100%

✅ Production-Ready Mobile Web App
```

## 🔧 **Customization**

### Adding New Specialists
```python
# In specialist_factory.py
elif agent_type == "my_specialist":
    base_prompt += """
- Focus ONLY on your domain expertise
- Use reflection to maintain quality
- Follow best practices for your field
"""
```

### Custom Mobile Tools
```python
# In mobile_tools.py
def create_custom_component(self, component_name: str) -> str:
    # Your custom mobile component logic
    return self.file_ops.write_file(f"src/components/{component_name}.tsx", content)
```

### Extending Reflection
```python
# In reflection.py
def custom_assessment(self, focus: str) -> str:
    # Your custom quality assessment logic
    return assessment_result
```

## 🎯 **Use Cases**

### **For Mobile Web Development**
- **Rapid Prototyping**: PRD → Working app in minutes
- **Component Libraries**: Automated responsive component creation
- **PWA Development**: Complete progressive web app setup
- **Performance Optimization**: Automated mobile performance testing

### **For Code Quality**
- **Automated Code Review**: Continuous quality assessment
- **Iterative Improvement**: Self-correcting code refinement
- **Security Analysis**: Automated vulnerability detection
- **Documentation Generation**: Smart comment and doc creation

### **For Team Productivity**
- **Sub-Agent Delegation**: Parallel specialist development
- **Quality Gates**: Consistent code standards enforcement
- **Testing Automation**: Comprehensive test suite generation
- **Integration Management**: Coordinated component integration

## 🔒 **Security & Safety**

- **Sandboxed Execution**: Operations limited to working directory
- **Quality Validation**: Automated security pattern detection
- **Error Recovery**: Graceful failure handling and retry logic
- **Tool Restrictions**: Safe bash command allowlisting

## 🤝 **Contributing**

This is an advanced autonomous system. Areas for contribution:

- **New Specialist Types**: DevOps, Security, Analytics agents
- **Enhanced Reflection**: More sophisticated self-assessment
- **Mobile Framework Support**: React Native, Flutter integration
- **Advanced Quality Gates**: Custom scoring algorithms

## 📈 **Performance**

- **Parallel Sub-Agents**: 3-5x faster than sequential development
- **Quality-First**: 80+ code quality scores standard
- **Mobile-Optimized**: Lighthouse performance scores >90
- **Self-Correcting**: Automatic issue detection and resolution

---

## 🎓 **Architecture Philosophy**

**Full Agent Autonomy**: Each sub-agent is a complete autonomous system with full capabilities, specialized through intelligent prompts rather than artificial tool restrictions.

**Reflection-Driven Quality**: Continuous self-assessment and improvement ensure production-ready output with minimal human intervention.

**Mobile-First Everything**: Every component, layout, and optimization prioritizes mobile user experience and performance.

*Built for the future of autonomous software development.*