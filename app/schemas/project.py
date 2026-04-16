# Pydantic Schemas or models that validate and serialize incoming and outgoing data for the Project
from pydantic import AnyHttpUrl, BaseModel, ConfigDict
from typing import List, Optional
import datetime


class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    github_backend: Optional[AnyHttpUrl] = None
    github_frontend: Optional[AnyHttpUrl] = None
    live_at: Optional[AnyHttpUrl] = None
    technologies: Optional[List[str]] = None


class ProjectOut(ProjectBase):
    id: int
    created_at: datetime.datetime | None

    # Allows Pydantic to read SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)
