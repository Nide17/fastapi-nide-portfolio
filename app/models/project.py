# DB Tables
from sqlalchemy import Column, Integer, String, ARRAY, TIMESTAMP, text
from app.db.session import Base
from typing import Any


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False, unique=True)
    description = Column(String)
    image = Column(String)
    github_backend = Column(String)
    github_frontend = Column(String)
    live_at = Column(String)
    # Array of strings like ["FastAPI", "React"]
    # Annotate as Any to satisfy static type checkers for SQLAlchemy descriptors
    technologies: Any = Column(ARRAY(String))
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("(NOW() AT TIME ZONE 'UTC')"))
