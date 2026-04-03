# DB Tables
from sqlalchemy import Column, Integer, String, ARRAY, DateTime
from app.db.session import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False, unique=True)
    description = Column(String)
    image = Column(String)
    github = Column(String)
    live_at = Column(String)
    technologies = Column(ARRAY(String)) # Array of strings like ["FastAPI", "React"]
    created_at = Column(DateTime)
