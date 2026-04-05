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
    visit_data.ip_address = str(visit_data.ip_address)  # Convert IPvAnyAddress to string for DB storage
    new_visit = Visit(**visit_data.model_dump())
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)
    return new_visit

def edit_visit(db: Session, visit_id: int, visit_data):
    """Updates an existing visit in the database."""
    visit_data.ip_address = str(visit_data.ip_address)
    db.query(Visit).filter(Visit.id == visit_id).update(visit_data.model_dump())
    db.commit()
    return db.query(Visit).filter(Visit.id == visit_id).first()

def remove_visit(db: Session, visit_id: int):
    """Deletes a visit from the database."""
    db.query(Visit).filter(Visit.id == visit_id).delete()
    db.commit()
