"""
main.py
-------
Responsibility: Create the FastAPI application, create the database
tables on startup, and register our routers.

This is the entry point of the whole app — this is the file you run.
"""

from fastapi import FastAPI

from app.database import Base, engine
from app.routes import task_routes

# This line creates all database tables that inherit from Base
# (in our case, just the 'tasks' table) IF they don't already exist.
#
# In a real production app, you'd normally use a migration tool like
# Alembic to manage schema changes over time (e.g. adding a column
# without losing existing data). For this beginner project, letting
# SQLAlchemy auto-create tables on startup is simpler and perfectly fine.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="To-Do List Backend",
    description="A simple, beginner-friendly REST API for managing to-do tasks, "
    "built with FastAPI, SQLAlchemy, and SQLite.",
    version="1.0.0",
)

# Register the task routes with the main app.
# Everything defined in task_routes.py (with its /tasks prefix)
# now becomes part of this app.
app.include_router(task_routes.router)


@app.get("/", tags=["Root"], summary="Health check")
def read_root():
    """Simple health-check endpoint to confirm the API is running."""
    return {"message": "To-Do List API is running. Visit /docs for API documentation."}
