import os
import yaml
import git
import logging
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManagerAgent:
    def __init__(self, knowledge_base_path: str = "../knowledge_base/knowledge_store.yaml"):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.sub_agents = {}
        self.current_tasks = {}
        self.initialize_knowledge_base()
        
    def initialize_knowledge_base(self):
        """Initialize or load the knowledge base."""
        if not self.knowledge_base_path.exists():
            initial_knowledge = {
                "project_standards": {
                    "coding_style": "PEP 8",
                    "git_workflow": "feature branch workflow",
                    "testing_requirements": ["unit tests", "integration tests"]
                },
                "system_prompts": {},
                "active_tasks": {},
                "completed_tasks": []
            }
            self.update_knowledge_base(initial_knowledge)
    
    def update_knowledge_base(self, data: dict):
        """Update the knowledge base with new information."""
        os.makedirs(self.knowledge_base_path.parent, exist_ok=True)
        with open(self.knowledge_base_path, 'w') as f:
            yaml.dump(data, f)
    
    def read_knowledge_base(self) -> dict:
        """Read the current state of the knowledge base."""
        with open(self.knowledge_base_path, 'r') as f:
            return yaml.safe_load(f)
    
    def assign_task(self, task_id: str, description: str, agent_type: str) -> bool:
        """Assign a task to a specific type of sub-agent."""
        if agent_type not in self.sub_agents:
            logger.error(f"No agent available for type: {agent_type}")
            return False
            
        knowledge_base = self.read_knowledge_base()
        knowledge_base["active_tasks"][task_id] = {
            "description": description,
            "agent": agent_type,
            "status": "assigned",
            "assigned_at": datetime.now().isoformat()
        }
        self.update_knowledge_base(knowledge_base)
        return True
    
    def update_task_status(self, task_id: str, status: str, output: Optional[str] = None):
        """Update the status of a task and record its output."""
        knowledge_base = self.read_knowledge_base()
        if task_id in knowledge_base["active_tasks"]:
            task = knowledge_base["active_tasks"][task_id]
            task["status"] = status
            task["last_updated"] = datetime.now().isoformat()
            if output:
                task["output"] = output
            
            if status == "completed":
                knowledge_base["completed_tasks"].append(
                    knowledge_base["active_tasks"].pop(task_id)
                )
            
            self.update_knowledge_base(knowledge_base)
    
    def trigger_tests(self) -> bool:
        """Trigger the test suite and log results."""
        try:
            import pytest
            result = pytest.main(["tests/"])
            return result == 0
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            return False
    
    def generate_progress_report(self) -> Dict:
        """Generate a summary of current project progress."""
        knowledge_base = self.read_knowledge_base()
        return {
            "active_tasks": len(knowledge_base["active_tasks"]),
            "completed_tasks": len(knowledge_base["completed_tasks"]),
            "blockers": [
                task for task in knowledge_base["active_tasks"].values()
                if task.get("status") == "blocked"
            ]
        }

if __name__ == "__main__":
    manager = ManagerAgent()
    logger.info("Manager Agent initialized successfully")
    # Example usage
    manager.assign_task(
        "TASK-001",
        "Implement user authentication API",
        "backend"
    )
