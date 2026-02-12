from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

tasks = []

@app.get("/")
def root():
    return {"message": "Task Manager API running"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    tasks.append(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t.id != task_id]
    return {"status": "deleted"}
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks[i] = updated_task
            return updated_task
    return {"error": "Task not found"}
