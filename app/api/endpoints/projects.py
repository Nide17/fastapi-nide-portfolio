# Routes for handling project-related API endpoints

from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/{project_id}", response_model=ProjectOut)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """Endpoint to fetch a specific project by its ID."""
    project = crud_project.get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
