# FastAPI Nide Portfolio

A small FastAPI for my portfolio API for managing projects, messages, downloads, visits, and authentication.

## Features

- Health check endpoint: `/health`
- Root welcome endpoint: `/`
- CRUD-style routers for:
  - `/projects`
  - `/messages`
  - `/downloads`
  - `/visits`
  - `/users`
- Interactive API docs at `/docs`
- Alembic migrations for database schema changes
- Docker-ready with `Dockerfile` and `docker-compose.yml`

## Quick Start

### Local Python

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Open the docs:

- `http://localhost:8000/docs`

### Docker

1. Build and run the container:

```bash
docker compose up --build
```

2. Visit the running API:

- `http://localhost:5000`
- `http://localhost:5000/docs`

> The Docker compose setup uses `.env-docker` for environment variables (defines DATABASE_URL) and exposes port `5000`.

## Adding a new route

To add a new API route, follow the repo's existing structure:

1. Create Pydantic schemas in `app/schemas/`
2. Add a SQLAlchemy model in `app/models/`
3. Add CRUD operations in `app/crud/`
4. Create a router in `app/api/endpoints/`
5. Register the router in `app/main.py`
6. Create and apply Alembic migrations

## Migrations

Use Alembic to keep the database schema in sync with models:

```bash
alembic revision --autogenerate -m "Add <description>"
alembic upgrade head
```

## Project structure

- `app/main.py` - FastAPI application entrypoint
- `app/api/endpoints/` - API routers
- `app/crud/` - CRUD helpers
- `app/models/` - SQLAlchemy models
- `app/schemas/` - Pydantic schemas
- `app/db/` - database session and configuration
- `migrations/` - Alembic migration files
- `Dockerfile` and `docker-compose.yml` - container setup

## License

This project is licensed under the MIT License. See `LICENSE`.
