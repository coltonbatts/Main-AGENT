import pytest
from pathlib import Path
from agents.utils import Task, TaskQueue, GitManager

def test_task_creation():
    task = Task("Test task", "backend", priority=2)
    assert task.description == "Test task"
    assert task.agent_type == "backend"
    assert task.priority == 2
    assert task.status == "pending"
    
def test_task_queue():
    queue = TaskQueue()
    task = Task("Test task", "frontend")
    
    # Test adding task
    task_id = queue.add_task(task)
    assert task_id == task.id
    
    # Test getting task
    retrieved_task = queue.get_task(task_id)
    assert retrieved_task.description == "Test task"
    
    # Test updating task status
    assert queue.update_task_status(task_id, "in_progress")
    assert queue.get_task(task_id).status == "in_progress"
    
def test_task_serialization():
    task = Task("Test task", "backend", priority=1)
    task_dict = task.to_dict()
    
    reconstructed_task = Task.from_dict(task_dict)
    assert reconstructed_task.id == task.id
    assert reconstructed_task.description == task.description
    assert reconstructed_task.agent_type == task.agent_type
    
@pytest.fixture
def temp_git_repo(tmp_path):
    return str(tmp_path / "test_repo")
    
def test_git_manager(temp_git_repo):
    # Initialize git repo
    git_manager = GitManager(temp_git_repo)
    
    # Create a test file and make initial commit
    test_file = Path(temp_git_repo) / "test.txt"
    test_file.write_text("initial content")
    assert git_manager.commit_changes(["test.txt"], "Initial commit")
    
    # Create and switch to new branch
    assert git_manager.create_branch("feature/test")
    assert git_manager.get_current_branch() == "feature/test"
    
    # Update the test file and commit
    test_file.write_text("updated content")
    assert git_manager.commit_changes(["test.txt"], "Test commit")
    
    # Try merging back to main
    assert git_manager.merge_branch("feature/test", "main")
