# This separates DB queries from API logic (routes)
from sqlalchemy.orm import Session
from app.models.visit import Visit


def get_all_visits(db: Session):
    """Fetches all visits from the database."""
    return db.query(Visit).all()


def get_visit_by_id(db: Session, visit_id: int):
    """Fetches a single visit by its ID."""
    return db.query(Visit).filter(Visit.id == visit_id).first()


def add_visit(db: Session, visit_data):
    """Creates a new visit in the database."""
    new_visit = Visit(**visit_data.model_dump())
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)
    return new_visit
