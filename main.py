from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# -------------------------------------------------
# DATABASE CONFIGURATION (SQLite)
# -------------------------------------------------

# SQLite database file (will be created automatically)
DATABASE_URL = "sqlite:///./tasks.db"

# Create database engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()

# -------------------------------------------------
# DATABASE MODEL (Table Schema)
# -------------------------------------------------

class TaskDB(Base):
    """
    SQLAlchemy model representing the tasks table.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(Boolean, default=False)

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# -------------------------------------------------
# FASTAPI APP INITIALIZATION
# -------------------------------------------------

app = FastAPI()

# -------------------------------------------------
# Pydantic Model (Request / Response Schema)
# -------------------------------------------------

class TaskBase(BaseModel):
    """
    Base Pydantic model for shared task fields.
    """
    title: str
    completed: bool = False

class TaskCreate(TaskBase):
    """
    Pydantic model for task creation.
    """
    pass

class Task(TaskBase):
    """
    Pydantic model used for API input/output validation.
    """
    id: int

    class Config:
        orm_mode = True

# -------------------------------------------------
# DATABASE DEPENDENCY
# -------------------------------------------------

def get_db():
    """
    Dependency that provides a database session per request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------------------------
# ROOT ENDPOINT
# -------------------------------------------------

@app.get("/")
def root():
    return {"message": "Task Manager API running with SQLite"}

# -------------------------------------------------
# GET ALL TASKS
# -------------------------------------------------

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    """
    Retrieve all tasks from the database.
    """
    return db.query(TaskDB).all()

# -------------------------------------------------
# CREATE NEW TASK
# -------------------------------------------------

@app.post("/tasks", response_model=Task)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Add a new task to the database.
    """
    db_task = TaskDB(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# -------------------------------------------------
# UPDATE EXISTING TASK
# -------------------------------------------------

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    """
    Update an existing task by ID.
    """
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not db_task:
        return {"error": "Task not found"}

    db_task.title = task.title  # type: ignore
    setattr(db_task, "completed", task.completed)
    db.commit()
    db.refresh(db_task)

    return db_task

# -------------------------------------------------
# DELETE TASK
# -------------------------------------------------

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by ID.
    """
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not db_task:
        return {"error": "Task not found"}

    db.delete(db_task)
    db.commit()

    return {"status": "deleted"}

