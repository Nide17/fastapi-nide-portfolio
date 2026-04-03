# This separates DB queries from API logic (routes)

from sqlalchemy.orm import Session
from app.models.project import Project

def get_all_projects(db: Session):
    """Fetches all projects from the database."""
    return db.query(Project).all()
