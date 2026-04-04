# This separates DB queries from API logic (routes)
from sqlalchemy.orm import Session
from app.models.project import Project

def get_all_projects(db: Session):
    """Fetches all projects from the database."""
    return db.query(Project).all()

def get_project_by_id(db: Session, project_id: int):
    """Fetches a single project by its ID."""
    return db.query(Project).filter(Project.id == project_id).first()
