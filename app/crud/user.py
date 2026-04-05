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


def add_user(db: Session, user_data):
    """Creates a new user in the database."""
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def edit_user(db: Session, user_id: int, user_data):
    """Updates an existing user in the database."""
    db.query(User).filter(User.id == user_id).update(user_data.model_dump())
    db.commit()
    return db.query(User).filter(User.id == user_id).first()


def remove_user(db: Session, user_id: int):
    """Deletes a user from the database."""
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
