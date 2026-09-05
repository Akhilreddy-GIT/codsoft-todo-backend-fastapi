"""
database.py
-----------
Responsibility: Set up the connection to our SQLite database and
provide a way for the rest of the app to talk to it.

This file does NOT define what a "Task" looks like (that's models/task.py).
It only sets up the plumbing: the engine, the session factory, and the Base
class that our models will inherit from.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# 1. Where is our database file?
# ---------------------------------------------------------
# "sqlite:///./todo.db" means: use SQLite, and store the database
# in a file called todo.db in the current folder (a local file, not a server).
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# ---------------------------------------------------------
# 2. The Engine
# ---------------------------------------------------------
# The "engine" is the actual connection to the database.
# Think of it as the phone line between our Python code and the SQLite file.
#
# connect_args={"check_same_thread": False} is SQLite-specific:
# by default, SQLite only allows the thread that created a connection
# to use it. FastAPI can handle requests using different threads,
# so we turn this restriction off. (This is a SQLite quirk only —
# you would NOT need this for PostgreSQL/MySQL.)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# ---------------------------------------------------------
# 3. The Session Factory
# ---------------------------------------------------------
# A "Session" is a temporary workspace where SQLAlchemy tracks
# any changes you make (add, update, delete) before you "commit" them
# to the actual database.
#
# SessionLocal is not a session itself — it's a FACTORY that creates
# new Session objects whenever we call SessionLocal().
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------------------------------------------
# 4. The Base class
# ---------------------------------------------------------
# All our database models (like Task) will inherit from this Base class.
# It's how SQLAlchemy knows "this Python class represents a database table."
Base = declarative_base()


def get_db():
    """
    This function creates a new database session for a single request,
    hands it over to whichever route needs it, and then ALWAYS closes it
    afterward — even if an error happened.

    We don't call this function ourselves. FastAPI calls it for us
    whenever a route uses Depends(get_db). More on this in routes/task_routes.py.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
