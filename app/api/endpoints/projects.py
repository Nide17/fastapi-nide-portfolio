# Routes for handling project-related API endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from app.db.session import get_db
from app.core import auth
from app.crud import project as crud_project
from app.schemas.project import ProjectBase, ProjectOut

router = APIRouter()


@router.get("/", response_model=list[ProjectOut])
def read_projects(db: Session = Depends(get_db)):
    """Endpoint to fetch all projects."""
    try:
        return crud_project.get_all_projects(db)
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed while fetching projects.",
        ) from exc
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Database error while fetching projects.",
        ) from exc


@router.get("/{project_id}", response_model=ProjectOut)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """Endpoint to fetch a specific project by its ID."""
    try:
        project = crud_project.get_project_by_id(db, project_id)
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed while fetching the project.",
        ) from exc
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Database error while fetching the project.",
        ) from exc
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectOut)
def create_project(project_data: ProjectBase, db: Session = Depends(get_db)):
    """Endpoint to create a new project."""
    try:
        return crud_project.add_project(db, project_data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A project with this title already exists.",
        ) from exc
    except OperationalError as exc:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Database connection failed while creating the project.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while creating the project.",
        ) from exc


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    project_data: ProjectBase,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    """Endpoint to update an existing project."""
    try:
        existing_project = crud_project.get_project_by_id(db, project_id)
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed while loading the project.",
        ) from exc
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Database error while loading the project.",
        ) from exc
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Admin access required")
    if existing_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    try:
        return crud_project.edit_project(db, project_id, project_data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A project with this title already exists.",
        ) from exc
    except OperationalError as exc:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Database connection failed while updating the project.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while updating the project.",
        ) from exc


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    """Endpoint to delete a project."""
    try:
        existing_project = crud_project.get_project_by_id(db, project_id)
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed while loading the project.",
        ) from exc
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Database error while loading the project.",
        ) from exc
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Admin access required")
    if existing_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    try:
        crud_project.remove_project(db, project_id)
    except OperationalError as exc:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Database connection failed while deleting the project.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error while deleting the project.",
        ) from exc
    return {"msg": "Project deleted successfully"}
