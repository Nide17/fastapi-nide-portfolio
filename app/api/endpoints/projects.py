# Routes for handling project-related API endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import project as crud_project
from app.schemas.project import ProjectBase, ProjectOut

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

@router.post("/", response_model=ProjectOut)
def create_project(project_data: ProjectBase, db: Session = Depends(get_db)):
    """Endpoint to create a new project."""
    project = crud_project.add_project(db, project_data)
    return project

@router.put("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, project_data: ProjectBase, db: Session = Depends(get_db)):
    """Endpoint to update an existing project."""
    existing_project = crud_project.get_project_by_id(db, project_id)
    if existing_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    updated_project = crud_project.edit_project(db, project_id, project_data)
    return updated_project
