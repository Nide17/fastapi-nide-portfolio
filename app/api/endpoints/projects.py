# Routes for handling project-related API endpoints

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import project as crud_project
from app.schemas.project import ProjectOut

router = APIRouter()

@router.get("/", response_model=list[ProjectOut])
def read_projects(db: Session = Depends(get_db)):
    """Endpoint to fetch all projects."""
    projects = crud_project.get_all_projects(db)
    return projects
