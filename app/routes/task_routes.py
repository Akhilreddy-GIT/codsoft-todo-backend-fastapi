"""
routes/task_routes.py
----------------------
Responsibility: Define the actual API endpoints (URLs + HTTP methods).

Routes are the "traffic cops" of the app:
- they receive the request
- they call the controller to do the real work
- they decide what HTTP status code / error to send back
- they do NOT contain database logic themselves

This keeps routes thin and readable.
"""

from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.controllers import task_controller

# APIRouter lets us define a group of related routes separately from
# main.py, then "plug them in" all at once. Think of it as a mini
# FastAPI app just for tasks, which main.py will register.
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new to-do task.

    - **title**: required, 1-100 characters
    - **description**: optional
    - **priority**: low / medium / high (defaults to medium)
    - New tasks always start as 'not completed'.
    """
    return task_controller.create_task(db, task_data)


@router.get(
    "",
    response_model=List[TaskResponse],
    summary="Get all tasks (optionally filtered)",
)
def get_tasks(
    completed: Optional[bool] = Query(
        None, description="Filter by completion status: true or false"
    ),
    search: Optional[str] = Query(
        None, description="Search tasks by title (case-insensitive)"
    ),
    db: Session = Depends(get_db),
):
    """
    Retrieve tasks.

    Why query parameters for filtering?
    Because `completed` and `search` are not part of the *resource path*
    (we're still asking for "tasks" in general) — they narrow down
    which tasks to return. That's exactly what query parameters are for,
    e.g. GET /tasks?completed=true&search=python
    """
    return task_controller.get_tasks(db, completed=completed, search=search)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a single task by id",
)
def get_task(
    task_id: int = Path(..., description="The id of the task to retrieve"),
    db: Session = Depends(get_db),
):
    """Retrieve one task. Returns 404 if it doesn't exist."""
    task = task_controller.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} was not found",
        )
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update an existing task",
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a task. Only send the fields you want to change —
    for example, {"completed": true} to mark a task done
    without touching its title or description.
    """
    task = task_controller.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} was not found",
        )
    return task_controller.update_task(db, task, task_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a task permanently.

    Returns 204 No Content on success — this status code means
    "it worked, and there's nothing meaningful to send back,"
    which fits a deletion perfectly.
    """
    task = task_controller.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} was not found",
        )
    task_controller.delete_task(db, task)
    return None
