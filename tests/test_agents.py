import pytest
import yaml
from pathlib import Path
from agents.manager_agent import ManagerAgent
from agents.frontend_agent import FrontendAgent
from agents.backend_agent import BackendAgent

@pytest.fixture
def test_knowledge_base(tmp_path):
    kb_path = tmp_path / "test_knowledge_base.yaml"
    initial_data = {
        "project_standards": {
            "coding_style": "PEP 8",
            "git_workflow": "feature branch workflow",
            "testing_requirements": ["unit tests", "integration tests"]
        },
        "active_tasks": {},
        "completed_tasks": []
    }
    with open(kb_path, 'w') as f:
        yaml.dump(initial_data, f)
    return kb_path

def test_manager_agent_initialization(test_knowledge_base):
    manager = ManagerAgent(str(test_knowledge_base))
    assert manager is not None
    
def test_task_assignment(test_knowledge_base):
    manager = ManagerAgent(str(test_knowledge_base))
    task_id = "TEST-001"
    description = "Test task"
    agent_type = "backend"
    
    # Task assignment should fail when no agents are registered
    assert not manager.assign_task(task_id, description, agent_type)
    
def test_frontend_agent_initialization(test_knowledge_base):
    frontend = FrontendAgent(str(test_knowledge_base))
    assert frontend is not None
    assert frontend.agent_type == "frontend"
    
def test_backend_agent_initialization(test_knowledge_base):
    backend = BackendAgent(str(test_knowledge_base))
    assert backend is not None
    assert backend.agent_type == "backend"
    
def test_knowledge_base_access(test_knowledge_base):
    manager = ManagerAgent(str(test_knowledge_base))
    kb_data = manager.read_knowledge_base()
    assert "project_standards" in kb_data
    assert "active_tasks" in kb_data
