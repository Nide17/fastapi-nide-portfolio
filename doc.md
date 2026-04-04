

### Alembic Migrations steps:
1. Install Alembic: `pip install alembic`
2. Initialize Alembic: `alembic init migrations`
3. Configure `env.py` to connect to the database.
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
4. Create a migration: `alembic revision -m "migration message"`.
5. Apply the migration: `alembic upgrade head`
6. To downgrade the migration: `alembic downgrade -1`

### Example:
```
alembic revision -m "Add user table"
alembic upgrade head
alembic downgrade -1
```
