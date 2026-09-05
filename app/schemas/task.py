"""
schemas/task.py
---------------
Responsibility: Define what data looks like coming IN from the client
(requests) and going OUT to the client (responses).

These are Pydantic models — completely separate from the SQLAlchemy
model in models/task.py. The SQLAlchemy model describes a database
table; these schemas describe API request/response shapes.

Why separate them? Because what a client is ALLOWED to send
(e.g. no 'id', no 'created_at') is different from what's stored in
the database (which has an id, timestamps, etc). Exposing the raw
SQLAlchemy model would leak internal fields and remove control over
validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.models.task import PriorityLevel


class TaskBase(BaseModel):
    """
    Shared fields between TaskCreate and TaskUpdate.
    Avoids repeating the same field definitions twice.
    """
    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Optional details")
    priority: PriorityLevel = Field(default=PriorityLevel.medium, description="low, medium, or high")
    category: Optional[str] = Field(None, max_length=50, description="Optional grouping label")
    due_date: Optional[datetime] = Field(None, description="Optional deadline")


class TaskCreate(TaskBase):
    """
    Used when a client creates a new task (POST /tasks).
    Inherits all fields from TaskBase — a new task always starts
    as 'not completed', so we don't let the client set that here.
    """
    pass


class TaskUpdate(BaseModel):
    """
    Used when a client updates an existing task (PUT /tasks/{id}).
    Every field is Optional — a client might only want to change
    the 'completed' status without resending the whole task.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None
    priority: Optional[PriorityLevel] = None
    category: Optional[str] = Field(None, max_length=50)
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    """
    Used when we SEND a task back to the client (in any endpoint).
    Includes fields the client never sends themselves, like id,
    completed, and timestamps — these are set by the server.
    """
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    # This tells Pydantic: "it's okay to build this schema directly
    # from a SQLAlchemy object's attributes" (task.id, task.title, etc),
    # not just from a plain dictionary.
    model_config = ConfigDict(from_attributes=True)
