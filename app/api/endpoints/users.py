"""
User-related endpoints: registration, login, password reset (forgot/reset) and basic CRUD.
"""

from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud import user as crud_user
from app.schemas.user import (
    UserBase,
    UserOut,
    UserCreate,
    UserLogin,
    Token as TokenSchema,
    PasswordResetRequest,
    PasswordResetConfirm,
)
from app.core import auth


router = APIRouter()


def ensure_self_or_admin(current_user, target_user_id: int) -> None:
    """Allow access when the caller owns the resource or is an admin."""
    if current_user.id == target_user_id or current_user.role == "admin":
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to access this user",
    )


def ensure_admin(current_user) -> None:
    """Allow access only to admins."""
    if current_user.role == "admin":
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin access required",
    )


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (hashes password)."""
    existing = crud_user.get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = crud_user.create_user(db, user_data)
    return user


@router.post("/login", response_model=TokenSchema)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    user = crud_user.authenticate_user(
        db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    data = {"sub": user.email, "id": user.id, "role": user.role}
    access_token = auth.create_access_token(data)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user=Depends(auth.get_current_user)):
    """Stateless logout: the client must discard stored bearer tokens."""
    _ = current_user
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """Issue a password reset token for the provided email and send via email."""
    from app.utils.email import send_reset_email
    user = crud_user.get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")
    token = auth.create_password_reset_token(str(user.email))
    name_to_use = request.name or str(user.name) or "User"
    await send_reset_email(request.email, name_to_use, token)
    return {"msg": "Password reset email sent. Check your inbox (or console in test mode)."}


@router.post("/reset-password")
def reset_password(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Reset password using a valid password-reset token."""
    payload = auth.decode_token(data.token)
    if not payload or payload.get("type") != "password_reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token payload")
    user = crud_user.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # Cast the user.id to int for static type checkers (it's a Column[int] descriptor at type-level).
    crud_user.update_user_password(db, cast(int, user.id), data.new_password)
    return {"msg": "Password has been reset successfully"}


@router.get("/me", response_model=UserOut)
def read_current_user(current_user=Depends(auth.get_current_user)):
    """Get the current authenticated user's profile."""
    return current_user


@router.get("/", response_model=list[UserOut])
def read_users(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    """Endpoint to fetch all users."""
    ensure_admin(current_user)
    users = crud_user.get_all_users(db)
    return users


@router.get("/email/{email}", response_model=UserOut)
def read_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    """Endpoint to fetch a specific user by their email."""
    user = crud_user.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    ensure_self_or_admin(current_user, user.id.scalar())
    return user


@router.get("/{user_id}", response_model=UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    """Endpoint to fetch a specific user by its ID."""
    ensure_self_or_admin(current_user, user_id)
    user = crud_user.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_data: UserBase,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    """Endpoint to update an existing user."""
    ensure_self_or_admin(current_user, user_id)
    user = crud_user.edit_user(db, user_id, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    """Endpoint to delete a specific user by its ID."""
    ensure_self_or_admin(current_user, user_id)
    existing_user = crud_user.get_user_by_id(db, user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.remove_user(db, user_id)
    return {"msg": "User deleted successfully"}
