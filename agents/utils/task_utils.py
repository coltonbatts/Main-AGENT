from typing import Dict, List, Optional
from datetime import datetime
import uuid

class Task:
    def __init__(self, description: str, agent_type: str, priority: int = 1):
        self.id = str(uuid.uuid4())
        self.description = description
        self.agent_type = agent_type
        self.priority = priority
        self.status = "pending"
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.assigned_to = None
        self.dependencies = []
        
    def to_dict(self) -> Dict:
        """Convert task to dictionary format."""
        return {
            "id": self.id,
            "description": self.description,
            "agent_type": self.agent_type,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "assigned_to": self.assigned_to,
            "dependencies": self.dependencies
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create a Task instance from dictionary data."""
        task = cls(data["description"], data["agent_type"], data["priority"])
        task.id = data["id"]
        task.status = data["status"]
        task.created_at = data["created_at"]
        task.updated_at = data["updated_at"]
        task.assigned_to = data["assigned_to"]
        task.dependencies = data["dependencies"]
        return task

class TaskQueue:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        
    def add_task(self, task: Task) -> str:
        """Add a task to the queue."""
        self.tasks[task.id] = task
        return task.id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """Update the status of a task."""
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            self.tasks[task_id].updated_at = datetime.now().isoformat()
            return True
        return False
    
    def get_tasks_by_agent(self, agent_type: str) -> List[Task]:
        """Get all tasks assigned to a specific agent type."""
        return [task for task in self.tasks.values() if task.agent_type == agent_type]
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        return [task for task in self.tasks.values() if task.status == "pending"]
