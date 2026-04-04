# This separates DB queries from API logic (routes)
from sqlalchemy.orm import Session
from app.models.user import User

def get_all_users(db: Session):
    """Fetches all users from the database."""
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    """Fetches a single user by its ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Fetches a single user by their email."""
    return db.query(User).filter(User.email == email).first()
