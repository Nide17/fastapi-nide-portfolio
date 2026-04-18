# This separates DB queries from API logic (routes)
from sqlalchemy.orm import Session
from app.models.project import Project


def get_all_projects(db: Session):
    """Fetches all projects from the database."""
    return db.query(Project).order_by(Project.created_at.asc()).all()


def get_project_by_id(db: Session, project_id: int):
    """Fetches a single project by its ID."""
    return db.query(Project).filter(Project.id == project_id).first()


def add_project(db: Session, project_data):
    """Creates a new project in the database."""
    data = project_data.model_dump()
    # Convert AnyHttpUrl to strings
    if data.get('github_backend') is not None:
        data['github_backend'] = str(data['github_backend'])
    if data.get('github_frontend') is not None:
        data['github_frontend'] = str(data['github_frontend'])
    if data.get('live_at') is not None:
        data['live_at'] = str(data['live_at'])
    # For technologies. data like FastAPI;PostgreSQL are a list, but if it's a single string, we need to convert it to a list
    if data.get('technologies') is not None and isinstance(data['technologies'], str):
        data['technologies'] = [data['technologies']]
    new_project = Project(**data)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


def edit_project(db: Session, project_id: int, project_data):
    """Updates an existing project in the database."""
    data = project_data.model_dump()
    if not isinstance(data, dict):
        data = dict(data)
    # Convert AnyHttpUrl to strings
    if data.get('github_backend') is not None:
        data['github_backend'] = str(data['github_backend'])
    if data.get('github_frontend') is not None:
        data['github_frontend'] = str(data['github_frontend'])
    if data.get('live_at') is not None:
        data['live_at'] = str(data['live_at'])
    # For technologies. data like FastAPI;PostgreSQL are a list, but if it's a single string, we need to convert it to a list
    if data.get('technologies') is not None and isinstance(data['technologies'], str):
        data['technologies'] = [data['technologies']]
    db.query(Project).filter(Project.id == project_id).update(data)
    db.commit()
    return db.query(Project).filter(Project.id == project_id).first()


def remove_project(db: Session, project_id: int):
    """Deletes a project from the database."""
    db.query(Project).filter(Project.id == project_id).delete()
    db.commit()
