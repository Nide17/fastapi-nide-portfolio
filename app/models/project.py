# DB Tables
from sqlalchemy import Column, Integer, String, ARRAY, TIMESTAMP, text
from app.db.session import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False, unique=True)
    description = Column(String)
    image = Column(String)
    github = Column(String)
    live_at = Column(String)
    # Array of strings like ["FastAPI", "React"]
    technologies = Column(ARRAY(String))
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("NOW() AT TIME ZONE 'UTC'"))
