"""
controllers/task_controller.py
-------------------------------
Responsibility: The actual business logic. Talks to the database
via SQLAlchemy, using data that's ALREADY validated by Pydantic.

Routes call these functions — routes themselves stay thin and only
deal with HTTP concerns (status codes, path/query params).
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate) -> Task:
    """Create a new Task row and save it to the database."""
    new_task = Task(**task_data.model_dump())
    db.add(new_task)       # stage the new task in this session
    db.commit()             # write it to the actual database file
    db.refresh(new_task)    # reload it so we get the server-generated id, timestamps, etc.
    return new_task


def get_tasks(
    db: Session,
    completed: Optional[bool] = None,
    search: Optional[str] = None,
) -> list[Task]:
    """
    Retrieve tasks, optionally filtered by completion status
    and/or a search term matched against the title.
    """
    query = db.query(Task)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    if search:
        # ilike = case-insensitive "contains" match (SQLite/Postgres both support it)
        query = query.filter(Task.title.ilike(f"%{search}%"))

    return query.all()


def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    """Retrieve a single task by its id, or None if it doesn't exist."""
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task: Task, task_data: TaskUpdate) -> Task:
    """
    Apply only the fields the client actually sent (exclude_unset=True)
    onto an existing Task object, then save the changes.
    """
    updates = task_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    """Remove a task from the database permanently."""
    db.delete(task)
    db.commit()
