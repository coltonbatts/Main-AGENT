from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import os
from database import Database

app = FastAPI(title="Multi-Agent Control Center")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize task storage (in-memory for serverless)
# tasks = []
# task_counter = 0

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
def root(request: Request):
    tasks = Database.get_tasks()
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
def create_task(task: TaskCreate):
    task_data = {
        "description": task.description,
        "agent_type": task.agent_type,
        "priority": task.priority,
        "status": "pending"
    }
    
    created_task = Database.create_task(task_data)
    if not created_task:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return created_task

@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    return Database.get_tasks()

@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    task = Database.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/tasks/{task_id}/status")
def update_task_status(task_id: str, status: str):
    updated_task = Database.update_task_status(task_id, status)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    success = Database.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
