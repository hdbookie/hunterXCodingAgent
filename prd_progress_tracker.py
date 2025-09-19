"""
PRD Progress Tracker for Autonomous Coding Agent

This module provides PRD parsing, progress tracking, and compliance checking
for the autonomous mobile surf coding agent.
"""

import json
import yaml
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

class PRDProgressTracker:
    """Tracks implementation progress against Product Requirements Document."""

    def __init__(self, prd_path: str = None):
        self.prd_path = prd_path
        self.prd = {}
        self.progress = {
            'entities': {},
            'workflows': {},
            'components': {},
            'tests': {},
            'deployment': {},
            'last_updated': None
        }

        if prd_path and os.path.exists(prd_path):
            self.load_prd(prd_path)

    def load_prd(self, prd_path: str) -> Dict[str, Any]:
        """Load and parse PRD from YAML or JSON file."""
        try:
            with open(prd_path, 'r', encoding='utf-8') as f:
                if prd_path.endswith('.yaml') or prd_path.endswith('.yml'):
                    self.prd = yaml.safe_load(f)
                else:
                    self.prd = json.load(f)

            self.prd_path = prd_path
            self._initialize_progress()
            return {"status": "success", "message": f"Loaded PRD from {prd_path}"}

        except Exception as e:
            return {"status": "error", "message": f"Failed to load PRD: {e}"}

    def _initialize_progress(self):
        """Initialize progress tracking structure based on PRD."""
        if not self.prd:
            return

        # Initialize entity progress
        for entity in self.prd.get('entities', {}):
            self.progress['entities'][entity] = {
                'model': False,
                'crud': False,
                'ui': False,
                'tests': False,
                'percentage': 0
            }

        # Initialize workflow progress
        for workflow in self.prd.get('workflows', []):
            workflow_name = workflow.get('name', '')
            self.progress['workflows'][workflow_name] = {
                'steps': {step: False for step in workflow.get('steps', [])},
                'percentage': 0
            }

        # Initialize component progress
        for component in self.prd.get('components', {}):
            self.progress['components'][component] = {
                'implemented': False,
                'tested': False,
                'percentage': 0
            }

        # Initialize test categories
        self.progress['tests'] = {
            'unit': 0,
            'integration': 0,
            'e2e': 0,
            'mobile': 0,
            'overall': 0
        }

        # Initialize deployment
        self.progress['deployment'] = {
            'database': False,
            'backend': False,
            'frontend': False,
            'domain': False,
            'ssl': False,
            'percentage': 0
        }

    def mark_entity_progress(self, entity_name: str, aspect: str, completed: bool = True) -> str:
        """Mark progress on entity implementation."""
        if entity_name not in self.progress['entities']:
            return f"ERROR: Entity '{entity_name}' not found in PRD"

        valid_aspects = ['model', 'crud', 'ui', 'tests']
        if aspect not in valid_aspects:
            return f"ERROR: Invalid aspect '{aspect}'. Valid: {valid_aspects}"

        self.progress['entities'][entity_name][aspect] = completed
        self._update_entity_percentage(entity_name)
        self._update_timestamp()

        return f"✅ Marked {entity_name}.{aspect} as {'completed' if completed else 'pending'}"

    def mark_workflow_progress(self, workflow_name: str, step: str, completed: bool = True) -> str:
        """Mark progress on workflow step."""
        if workflow_name not in self.progress['workflows']:
            return f"ERROR: Workflow '{workflow_name}' not found in PRD"

        if step not in self.progress['workflows'][workflow_name]['steps']:
            return f"ERROR: Step '{step}' not found in workflow '{workflow_name}'"

        self.progress['workflows'][workflow_name]['steps'][step] = completed
        self._update_workflow_percentage(workflow_name)
        self._update_timestamp()

        return f"✅ Marked {workflow_name}.{step} as {'completed' if completed else 'pending'}"

    def mark_component_progress(self, component_name: str, aspect: str, completed: bool = True) -> str:
        """Mark progress on component implementation."""
        if component_name not in self.progress['components']:
            return f"ERROR: Component '{component_name}' not found in PRD"

        valid_aspects = ['implemented', 'tested']
        if aspect not in valid_aspects:
            return f"ERROR: Invalid aspect '{aspect}'. Valid: {valid_aspects}"

        self.progress['components'][component_name][aspect] = completed
        self._update_component_percentage(component_name)
        self._update_timestamp()

        return f"✅ Marked {component_name}.{aspect} as {'completed' if completed else 'pending'}"

    def mark_deployment_progress(self, aspect: str, completed: bool = True) -> str:
        """Mark progress on deployment."""
        valid_aspects = ['database', 'backend', 'frontend', 'domain', 'ssl']
        if aspect not in valid_aspects:
            return f"ERROR: Invalid aspect '{aspect}'. Valid: {valid_aspects}"

        self.progress['deployment'][aspect] = completed
        self._update_deployment_percentage()
        self._update_timestamp()

        return f"✅ Marked deployment.{aspect} as {'completed' if completed else 'pending'}"

    def _update_entity_percentage(self, entity_name: str):
        """Update percentage completion for entity."""
        entity = self.progress['entities'][entity_name]
        completed = sum(1 for aspect in ['model', 'crud', 'ui', 'tests'] if entity[aspect])
        entity['percentage'] = int((completed / 4) * 100)

    def _update_workflow_percentage(self, workflow_name: str):
        """Update percentage completion for workflow."""
        workflow = self.progress['workflows'][workflow_name]
        steps = workflow['steps']
        if not steps:
            return
        completed = sum(1 for step in steps.values() if step)
        workflow['percentage'] = int((completed / len(steps)) * 100)

    def _update_component_percentage(self, component_name: str):
        """Update percentage completion for component."""
        component = self.progress['components'][component_name]
        completed = sum(1 for aspect in ['implemented', 'tested'] if component[aspect])
        component['percentage'] = int((completed / 2) * 100)

    def _update_deployment_percentage(self):
        """Update deployment percentage."""
        deployment = self.progress['deployment']
        aspects = ['database', 'backend', 'frontend', 'domain', 'ssl']
        completed = sum(1 for aspect in aspects if deployment[aspect])
        deployment['percentage'] = int((completed / len(aspects)) * 100)

    def _update_timestamp(self):
        """Update last modified timestamp."""
        self.progress['last_updated'] = datetime.now().isoformat()

    def get_overall_progress(self) -> int:
        """Calculate overall project completion percentage."""
        if not self.prd:
            return 0

        total_weight = 0
        total_progress = 0

        # Entities (40% weight)
        if self.progress['entities']:
            entity_avg = sum(e['percentage'] for e in self.progress['entities'].values()) / len(self.progress['entities'])
            total_progress += entity_avg * 0.4
            total_weight += 0.4

        # Workflows (25% weight)
        if self.progress['workflows']:
            workflow_avg = sum(w['percentage'] for w in self.progress['workflows'].values()) / len(self.progress['workflows'])
            total_progress += workflow_avg * 0.25
            total_weight += 0.25

        # Components (20% weight)
        if self.progress['components']:
            component_avg = sum(c['percentage'] for c in self.progress['components'].values()) / len(self.progress['components'])
            total_progress += component_avg * 0.2
            total_weight += 0.2

        # Deployment (15% weight)
        total_progress += self.progress['deployment']['percentage'] * 0.15
        total_weight += 0.15

        return int(total_progress / total_weight) if total_weight > 0 else 0

    def generate_progress_dashboard(self) -> str:
        """Generate a comprehensive progress dashboard."""
        if not self.prd:
            return "❌ No PRD loaded. Use load_prd(path) first."

        dashboard = f"""
🌊 SURF APP DEVELOPMENT PROGRESS DASHBOARD
PRD: {self.prd_path}
Last Updated: {self.progress.get('last_updated', 'Never')}

📊 OVERALL PROGRESS: {self.get_overall_progress()}%
{'='*50}

🗄️ ENTITIES ({len(self.progress['entities'])} total):
"""

        for entity, progress in self.progress['entities'].items():
            status_bar = self._create_progress_bar(progress['percentage'])
            dashboard += f"  {entity:<20} {status_bar} {progress['percentage']}%\n"
            dashboard += f"    Model: {'✅' if progress['model'] else '❌'} "
            dashboard += f"CRUD: {'✅' if progress['crud'] else '❌'} "
            dashboard += f"UI: {'✅' if progress['ui'] else '❌'} "
            dashboard += f"Tests: {'✅' if progress['tests'] else '❌'}\n"

        dashboard += f"\n⚡ WORKFLOWS ({len(self.progress['workflows'])} total):\n"
        for workflow, progress in self.progress['workflows'].items():
            status_bar = self._create_progress_bar(progress['percentage'])
            dashboard += f"  {workflow:<20} {status_bar} {progress['percentage']}%\n"
            for step, completed in progress['steps'].items():
                dashboard += f"    - {step}: {'✅' if completed else '❌'}\n"

        dashboard += f"\n🎨 COMPONENTS ({len(self.progress['components'])} total):\n"
        for component, progress in self.progress['components'].items():
            status_bar = self._create_progress_bar(progress['percentage'])
            dashboard += f"  {component:<20} {status_bar} {progress['percentage']}%\n"
            dashboard += f"    Implemented: {'✅' if progress['implemented'] else '❌'} "
            dashboard += f"Tested: {'✅' if progress['tested'] else '❌'}\n"

        deployment = self.progress['deployment']
        dashboard += f"\n🚀 DEPLOYMENT:\n"
        status_bar = self._create_progress_bar(deployment['percentage'])
        dashboard += f"  Overall {status_bar} {deployment['percentage']}%\n"
        dashboard += f"  Database: {'✅' if deployment['database'] else '❌'} "
        dashboard += f"Backend: {'✅' if deployment['backend'] else '❌'} "
        dashboard += f"Frontend: {'✅' if deployment['frontend'] else '❌'}\n"
        dashboard += f"  Domain: {'✅' if deployment['domain'] else '❌'} "
        dashboard += f"SSL: {'✅' if deployment['ssl'] else '❌'}\n"

        # Next priorities
        dashboard += f"\n🎯 NEXT PRIORITIES:\n"
        priorities = self.get_next_priorities()
        for i, priority in enumerate(priorities[:3], 1):
            dashboard += f"  {i}. {priority}\n"

        return dashboard

    def _create_progress_bar(self, percentage: int, width: int = 20) -> str:
        """Create ASCII progress bar."""
        filled = int((percentage / 100) * width)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}]"

    def get_next_priorities(self) -> List[str]:
        """Get next priority tasks based on current progress."""
        priorities = []

        # Check incomplete entities
        for entity, progress in self.progress['entities'].items():
            if not progress['model']:
                priorities.append(f"Create {entity} database model")
            elif not progress['crud']:
                priorities.append(f"Implement {entity} CRUD operations")
            elif not progress['ui']:
                priorities.append(f"Build {entity} UI components")
            elif not progress['tests']:
                priorities.append(f"Add tests for {entity}")

        # Check incomplete workflows
        for workflow, progress in self.progress['workflows'].items():
            for step, completed in progress['steps'].items():
                if not completed:
                    priorities.append(f"Implement {workflow}: {step}")

        # Check deployment
        deployment = self.progress['deployment']
        if not deployment['database']:
            priorities.append("Set up database schema")
        elif not deployment['backend']:
            priorities.append("Deploy backend services")
        elif not deployment['frontend']:
            priorities.append("Deploy frontend application")

        return priorities

    def validate_against_prd(self, project_path: str) -> Dict[str, Any]:
        """Validate current implementation against PRD requirements."""
        if not self.prd:
            return {"error": "No PRD loaded"}

        validation = {
            "compliance_score": 0,
            "missing_entities": [],
            "missing_workflows": [],
            "missing_components": [],
            "extra_implementations": [],
            "recommendations": []
        }

        # This would analyze the actual codebase and compare to PRD
        # For now, return progress-based validation
        validation["compliance_score"] = self.get_overall_progress()

        # Find missing implementations
        for entity, progress in self.progress['entities'].items():
            if progress['percentage'] < 100:
                validation["missing_entities"].append(f"{entity} ({progress['percentage']}% complete)")

        for workflow, progress in self.progress['workflows'].items():
            if progress['percentage'] < 100:
                validation["missing_workflows"].append(f"{workflow} ({progress['percentage']}% complete)")

        # Generate recommendations
        if validation["compliance_score"] < 50:
            validation["recommendations"].append("Focus on core entity implementation first")
        elif validation["compliance_score"] < 80:
            validation["recommendations"].append("Complete workflow implementations")
        else:
            validation["recommendations"].append("Focus on testing and deployment")

        return validation

    def export_progress(self, output_path: str) -> str:
        """Export progress data to JSON file."""
        try:
            export_data = {
                "prd_path": self.prd_path,
                "progress": self.progress,
                "overall_completion": self.get_overall_progress(),
                "next_priorities": self.get_next_priorities()[:5],
                "exported_at": datetime.now().isoformat()
            }

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)

            return f"✅ Progress exported to {output_path}"

        except Exception as e:
            return f"❌ Export failed: {e}"

def test_prd_progress_tracker():
    """Test the PRD progress tracker with sample data."""

    # Create sample PRD
    sample_prd = {
        "entities": {
            "user": {
                "fields": ["id", "email", "name", "role"],
                "relationships": ["sessions", "progress"]
            },
            "session": {
                "fields": ["id", "title", "date", "max_students"],
                "relationships": ["instructor", "students"]
            }
        },
        "workflows": [
            {
                "name": "book_session",
                "steps": ["browse_sessions", "select_session", "confirm_booking"]
            },
            {
                "name": "track_progress",
                "steps": ["assess_skills", "record_progress", "update_profile"]
            }
        ],
        "components": {
            "dashboard": {
                "widgets": ["upcoming_sessions", "progress_chart"]
            },
            "scheduler": {
                "features": ["time_slots", "availability"]
            }
        }
    }

    # Save sample PRD
    with open("sample_prd.yaml", "w") as f:
        yaml.dump(sample_prd, f)

    # Test tracker
    tracker = PRDProgressTracker("sample_prd.yaml")

    # Mark some progress
    print(tracker.mark_entity_progress("user", "model", True))
    print(tracker.mark_entity_progress("user", "crud", True))
    print(tracker.mark_workflow_progress("book_session", "browse_sessions", True))
    print(tracker.mark_component_progress("dashboard", "implemented", True))
    print(tracker.mark_deployment_progress("database", True))

    # Generate dashboard
    print(tracker.generate_progress_dashboard())

    # Export progress
    print(tracker.export_progress("progress_report.json"))

    print("✅ PRD Progress Tracker test completed")

if __name__ == "__main__":
    test_prd_progress_tracker()