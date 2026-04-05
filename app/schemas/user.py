# Pydantic Schemas or models that validate and serialize incoming and outgoing data for the User
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = None  # Can be used for admin or regular user roles


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime.datetime | None

    # Allows Pydantic to read SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)
