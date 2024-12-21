from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from agents import ManagerAgent, FrontendAgent, BackendAgent
from agents.utils import Task, TaskQueue

app = FastAPI(title="Multi-Agent Control Center")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize agents
manager = ManagerAgent()
frontend = FrontendAgent()
backend = BackendAgent()
task_queue = TaskQueue()

class TaskCreate(BaseModel):
    description: str
    agent_type: str
    priority: int = 1

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Get current status of all agents and tasks
    manager_status = "Processing tasks..."
    frontend_status = "Monitoring UI components..."
    backend_status = "API endpoints operational..."
    
    tasks = task_queue.get_pending_tasks()
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "manager_status": manager_status,
            "frontend_status": frontend_status,
            "backend_status": backend_status,
            "tasks": tasks
        }
    )

@app.post("/api/tasks")
async def create_task(task: TaskCreate):
    new_task = Task(
        description=task.description,
        agent_type=task.agent_type,
        priority=task.priority
    )
    task_id = task_queue.add_task(new_task)
    
    # Assign task to appropriate agent
    if task.agent_type == "frontend":
        frontend.process_task(task_id, new_task.to_dict())
    elif task.agent_type == "backend":
        backend.process_task(task_id, new_task.to_dict())
    
    return {"task_id": task_id}

@app.get("/api/tasks")
async def get_tasks():
    return {"tasks": [task.to_dict() for task in task_queue.get_pending_tasks()]}

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    task = task_queue.get_task(task_id)
    if task:
        return task.to_dict()
    return {"error": "Task not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
