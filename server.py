from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="Multi-Agent Control Center")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize task storage (in-memory for serverless)
tasks = []
task_counter = 0

class TaskCreate(BaseModel):
    description: str
    agent_type: str
    priority: int = 1

class Task(BaseModel):
    id: str
    description: str
    agent_type: str
    priority: int
    status: str = "pending"

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tasks": tasks,
            "manager_status": "Active",
            "frontend_status": "Processing tasks",
            "backend_status": "Ready"
        }
    )

@app.post("/api/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    global task_counter
    task_counter += 1
    new_task = Task(
        id=str(task_counter),
        description=task.description,
        agent_type=task.agent_type,
        priority=task.priority
    )
    tasks.append(new_task)
    return new_task

@app.get("/api/tasks", response_model=List[Task])
async def get_tasks():
    return tasks

@app.get("/api/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            return task
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
