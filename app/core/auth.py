from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import user as crud_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme expecting token from /users/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def verify_password(plain_password: str, hashed_password: Any) -> bool:
    """Verify a plain password against a hashed password.

    Some static type checkers (Pylance) may interpret SQLAlchemy mapped
    attributes as Column[...] objects rather than runtime strings. Accept
    Any here and coerce to str at runtime to avoid type complaints while
    preserving runtime behavior.
    """
    # Coerce to str in case a typing-aware analyzer exposed a Column type.
    if not isinstance(hashed_password, str):
        try:
            hashed_password = str(hashed_password)
        except Exception:
            # If coercion fails, treat as verification failure
            return False
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)


def create_access_token(data: dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    # Use timezone-aware UTC datetimes and encode `exp` as an int timestamp
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(
            timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # JWT expects numeric 'exp' (seconds since epoch). Use int timestamp.
    to_encode["exp"] = int(expire.timestamp())
    to_encode["type"] = "access"
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict[str, Any]) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    # Use timezone-aware now and numeric timestamp for 'exp'.
    expire = datetime.now(timezone.utc) + \
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode["exp"] = int(expire.timestamp())
    to_encode["type"] = "refresh"
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict[str, Any]]:
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Dependency to retrieve current user from an access token."""
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials")
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = crud_user.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def create_password_reset_token(email: str) -> str:
    """Create a password reset token."""
    # Explicitly type the dict so static checkers know values can be Any.
    to_encode: dict[str, Any] = {"sub": email, "type": "password_reset"}
    expire = datetime.now(
        timezone.utc) + timedelta(hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
    to_encode["exp"] = int(expire.timestamp())
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
