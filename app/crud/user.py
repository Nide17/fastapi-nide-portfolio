"""This separates DB queries from API logic (routes)"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.auth import get_password_hash, verify_password
from app.schemas.user import UserCreate


def get_all_users(db: Session):
    """Fetches all users from the database."""
    return db.query(User).order_by(User.created_at.desc()).all()


def get_user_by_id(db: Session, user_id: int):
    """Fetches a single user by its ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Fetches a single user by their email."""
    return db.query(User).filter(User.email == email).first()


def add_user(db: Session, user_data):
    """Creates a new user in the database from a mapping.

    Note: this is a low-level helper that expects the mapping keys to match
    the SQLAlchemy model (e.g., password_hash). Prefer `create_user` for
    creating users from user input (it hashes the password).
    """
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_user(db: Session, user: UserCreate):
    """Create a new user hashing the provided password."""
    user_dict = user.model_dump()
    password = user_dict.pop("password")
    user_dict["password_hash"] = get_password_hash(password)
    new_user = User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str):
    """Verify email and password. Return user if valid, else None."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def edit_user(db: Session, user_id: int, user_data):
    """Updates an existing user in the database."""
    data = user_data.model_dump()
    if not isinstance(data, dict):
        data = dict(data)
    db.query(User).filter(User.id == user_id).update(data)
    db.commit()
    return db.query(User).filter(User.id == user_id).first()


def remove_user(db: Session, user_id: int):
    """Deletes a user from the database."""
    db.query(User).filter(User.id == user_id).delete()
    db.commit()


def update_user_password(db: Session, user_id: int, new_password: str):
    """Update a user's password (hashed)."""
    hashed = get_password_hash(new_password)
    db.query(User).filter(User.id == user_id).update({"password_hash": hashed})
    db.commit()
    return db.query(User).filter(User.id == user_id).first()
