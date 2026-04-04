
### Adding a New route: eg. Messages
1. Create a new file `app/schemas/message.py` for the message-related Pydantic models (schemas).
2. Create a new SQLAlchemy model for messages in `app/models/message.py`.
3. Define the necessary CRUD operations in `app/crud/message.py`.
4. Create a new API endpoint file `app/api/endpoints/messages.py`. This file will contain the FastAPI router and the route definitions for the messages.
5. Include the new router in `app/main.py` to make the endpoints available.
6. Create and apply database migrations using Alembic to reflect the new model in the database schema, as described in the next section.
7. Test the new endpoints using tools like Postman or FastAPI's interactive docs at `/docs`.

### Database Migrations with Alembic

When you make changes to your SQLAlchemy models (like adding a new model, changing a column, etc.), you need to create and apply database migrations to keep your database schema in sync with your models.

Alembic is a popular tool for handling database migrations in Python projects that use SQLAlchemy.
### Alembic Migrations steps:
1. Install Alembic: `pip install alembic`: If it is not already installed.
2. Initialize Alembic: `alembic init migrations`: If it is not already initialized. This creates a `migrations` directory with the necessary configuration files.
3. Configure `env.py` to connect to the database: If not already set up.
   1. In `env.py`, import the models and set up the target metadata for autogeneration.
   2. Example `env.py` configuration:
   ```python
    # Import Base and models to ensure they are registered with Alembic for autogeneration.
        from app.db.session import Base, engine
        from app.models.project import Project
    
    # add model's MetaData object here
    target_metadata = Base.metadata

    # Adapt run_migrations_offline function like:
    url = str(engine.url)

    # Adapt run_migrations_online function like:
    connectable = engine
   ```
4. Create a migration: `alembic revision --autogenerate -m "migration message"`. The `--autogenerate` flag will automatically generate the migration script based on the differences between the current database schema and the models. This will ensure that the migration script is always up-to-date with the models.
5. Apply the migration: `alembic upgrade head`.
6. To downgrade the migration: `alembic downgrade -1`
7. Use `alembic stamp base` to mark the current state of the database as the base version if you are starting with an existing database and want to use Alembic for future migrations or if you want to reset the migration history.
8. Use `alembic stamp head` to mark the current state of the database as the latest version if you want to skip applying all existing migrations and start fresh from the current state.

### Example:
```
alembic revision --autogenerate -m "Add project table"
alembic upgrade head
alembic downgrade -1
```
