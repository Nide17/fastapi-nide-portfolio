# Routes for handling user-related API endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import user as crud_user
from app.schemas.user import UserBase, UserOut

router = APIRouter()

@router.get("/", response_model=list[UserOut])
def read_users(db: Session = Depends(get_db)):
    """Endpoint to fetch all users."""
    users = crud_user.get_all_users(db)
    return users

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Endpoint to fetch a specific user by its ID."""
    user = crud_user.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/email/{email}", response_model=UserOut)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    """Endpoint to fetch a specific user by their email."""
    user = crud_user.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserOut)
def create_user(user_data: UserBase, db: Session = Depends(get_db)):
    """Endpoint to create a new user."""
    user = crud_user.add_user(db, user_data)
    return user
