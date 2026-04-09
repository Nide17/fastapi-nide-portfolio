# Pydantic Schemas or models that validate and serialize incoming and outgoing data for the User
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class UserCreateOut(UserBase):
    id: int
    created_at: datetime.datetime | None

    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBase):
    id: int
    created_at: datetime.datetime | None

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    user_id: int | None = None
    email: str | None = None
