"""
models/task.py
--------------
Responsibility: Define what a "Task" looks like AS A DATABASE TABLE.

This is a SQLAlchemy model — it maps directly to a table in SQLite.
It has NOTHING to do with validating user input; that's the job of
schemas/task.py. This file only describes storage.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
import enum

from app.database import Base


class PriorityLevel(str, enum.Enum):
    """
    Bonus feature: restrict priority to a fixed set of values.
    Using a Python Enum means the database (and Pydantic later)
    will only ever accept 'low', 'medium', or 'high' — never a typo.
    """
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base):
    """
    This class represents the 'tasks' table in our SQLite database.
    Each attribute below becomes a column in that table.
    """

    __tablename__ = "tasks"

    # Primary key: unique identifier for each task, auto-incremented by SQLite.
    id = Column(Integer, primary_key=True, index=True)

    # Core required fields
    title = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)

    # Bonus fields
    priority = Column(Enum(PriorityLevel), default=PriorityLevel.medium, nullable=False)
    category = Column(String(50), nullable=True)
    due_date = Column(DateTime, nullable=True)

    # Timestamps — useful for showing when a task was created/last changed.
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
