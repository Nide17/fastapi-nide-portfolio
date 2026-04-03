# Set's up the db session for the app, handles dependency injection for db session in routes.
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine manages the pool of connections to the database, handles connection creation and pooling.
engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal is a factory for creating new Session objects, which are used to interact with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models, provides a common base for all models to inherit from.
class Base(DeclarativeBase):
    """Parent class for all SQLAlchemy models."""
    pass

# Dependency to inject the database session into routes, ensures that the session is properly closed after use.
def get_db():
    """Provides a database session to routes, ensures proper cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
