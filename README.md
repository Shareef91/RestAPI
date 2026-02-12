# Task Manager REST API (FastAPI)

A lightweight REST API for managing tasks (create, list, delete) built with **FastAPI**. It’s designed as a simple, clean starter project for learning or prototyping.

> Note: This API uses an **in-memory** list for storage. Tasks reset when the server restarts.

## Features

- FastAPI-powered REST endpoints
- Request validation via Pydantic models
- Interactive API docs (Swagger UI) out of the box
- Simple CRUD-style flow (List / Create / Delete)

## Tech Stack

- Python 3.9+
- FastAPI
- Pydantic
- Uvicorn (development server)

## Project Structure

- `main.py` — FastAPI application and routes
- `images/` — screenshots used in this README

## Getting Started

### 1) Create and activate a virtual environment (recommended)

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) Run the API

```powershell
uvicorn main:app --reload
```

FastAPI will expose interactive documentation (Swagger UI / ReDoc) automatically when the server is running.

## API Reference

### `GET /`

Health-check style endpoint.

**Response**

```json
{ "message": "Task Manager API running" }
```

### `GET /tasks`

Returns all tasks currently in memory.

**Response**

```json
[
  { "id": 1, "title": "Buy milk", "completed": false }
]
```

### `POST /tasks`

Creates a new task.

**Request body**

```json
{ "id": 1, "title": "Buy milk", "completed": false }
```

**Response**

Returns the created task.

### `DELETE /tasks/{task_id}`

Deletes a task by its `id`.

**Response**

```json
{ "status": "deleted" }
```

## Screenshots

### Swagger UI

![Swagger UI](images/Swagger%20UI.png)

### POST /tasks example

![POST example](images/POST.png)

### Quick test run

![Test run](images/TEST.png)

## Notes / Limitations

- Storage is **not persistent** (in-memory only).
- No update endpoint yet.
- No uniqueness checks for `id` (clients should avoid duplicates).

## Next Improvements (Optional)

- Add `PUT /tasks/{task_id}` to update a task
- Auto-generate IDs on the server
- Persist tasks using SQLite (via SQLModel or SQLAlchemy)
- Add basic tests with `pytest`
