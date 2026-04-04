# Pydantic Schemas or models that validate and serialize incoming and outgoing data for the Project
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import datetime

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    github: Optional[str] = None
    live_at: Optional[str] = None
    technologies: Optional[List[str]] = None

class ProjectOut(ProjectBase):
    id: int
    created_at: datetime.datetime | None

    model_config = ConfigDict(from_attributes=True) # Allows Pydantic to read SQLAlchemy objects
