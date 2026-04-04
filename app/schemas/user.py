# Pydantic Schemas or models that validate and serialize incoming and outgoing data for the User
from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    role: Optional[str] = None # Can be used for admin or regular user roles

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True) # Allows Pydantic to read SQLAlchemy objects
