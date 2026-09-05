# To-Do List Backend API

A clean, RESTful backend service for managing to-do tasks — built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

This project was built as part of my CodSoft Backend Development Internship (Task 3), with a focus on writing beginner-readable code organized around professional backend architecture: clear separation between routes, controllers, database models, and request/response schemas.

---

## Features

- Full CRUD for tasks (Create, Read, Update, Delete)
- Mark tasks as completed or pending
- Filter tasks by completion status (`completed=true` / `completed=false`)
- Search tasks by title (`search=keyword`)
- Bonus fields: priority level (low/medium/high), category, due date
- Automatic request validation with clear error messages
- Proper HTTP status codes for every response
- Auto-generated interactive API docs (Swagger UI + ReDoc)

---

## Technologies Used

| Technology | Purpose |
|---|---|
| **FastAPI** | Web framework for building the REST API |
| **Uvicorn** | ASGI server to run the FastAPI app |
| **SQLAlchemy** | ORM — maps Python classes to database tables |
| **Pydantic** | Request/response validation and serialization |
| **SQLite** | Lightweight file-based database |

---

## Project Structure

```
todo_backend/
├── app/
│   ├── main.py                     # Creates the FastAPI app, registers routes
│   ├── database.py                 # Database engine, session, and base setup
│   ├── models/
│   │   └── task.py                 # SQLAlchemy Task table definition
│   ├── schemas/
│   │   └── task.py                 # Pydantic request/response schemas
│   ├── controllers/
│   │   └── task_controller.py      # Business logic — talks to the database
│   └── routes/
│       └── task_routes.py          # API endpoints — HTTP concerns only
├── requirements.txt
├── README.md
└── .gitignore
```

**Why this structure?** Each layer has exactly one job:
- `routes` handle HTTP (status codes, request/response shape)
- `controllers` handle logic (what happens when a task is created/updated)
- `schemas` validate what comes in and shape what goes out
- `models` define what's actually stored in the database

This keeps each file small and focused, and makes the codebase easy to explain and extend.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Akhilreddy-GIT/<repo-name>.git
cd todo_backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Project

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

- Interactive Swagger docs: `http://127.0.0.1:8000/docs`
- ReDoc documentation: `http://127.0.0.1:8000/redoc`

The SQLite database file (`todo.db`) and its `tasks` table are created automatically the first time the app runs — no manual database setup needed.

> **Note:** In a production application, schema changes would typically be managed with a migration tool like Alembic. For this project's scope, automatic table creation on startup keeps things simple.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/tasks` | Create a new task |
| `GET` | `/tasks` | Get all tasks (supports `completed=` and `search=`) |
| `GET` | `/tasks/{task_id}` | Get a single task by ID |
| `PUT` | `/tasks/{task_id}` | Update a task (partial updates supported) |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

---

## Example Requests & Responses

### Create a task
`POST /tasks`
```json
{
  "title": "Learn FastAPI",
  "description": "Finish Task 3",
  "priority": "high"
}
```
**Response — `201 Created`**
```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Finish Task 3",
  "priority": "high",
  "category": null,
  "due_date": null,
  "completed": false,
  "created_at": "2026-09-05T09:50:03.438726",
  "updated_at": "2026-09-05T09:50:03.438732"
}
```

### Mark a task completed (partial update)
`PUT /tasks/1`
```json
{ "completed": true }
```
**Response — `200 OK`** — only `completed` and `updated_at` change; every other field stays the same.

### Filter and search
```
GET /tasks?completed=true
GET /tasks?search=fastapi
```

### Request a non-existent task
`GET /tasks/999`
**Response — `404 Not Found`**
```json
{ "detail": "Task with id 999 was not found" }
```

---

## HTTP Status Codes Used

| Code | Meaning | When |
|---|---|---|
| `200 OK` | Success | GET, PUT |
| `201 Created` | Resource created | POST |
| `204 No Content` | Success, nothing to return | DELETE |
| `404 Not Found` | Resource doesn't exist | GET/PUT/DELETE on a missing task |
| `422 Unprocessable Entity` | Invalid request body | Failed Pydantic validation |

---

## Future Improvements

- User authentication (JWT) so tasks belong to individual users
- PostgreSQL for production-grade persistence
- Alembic migrations for schema changes
- Pagination on `GET /tasks` for large datasets
- Automated test suite with pytest

---

## Author

Built by **Akhil** as part of the CodSoft Backend Development Internship.
