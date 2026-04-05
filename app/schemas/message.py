# Pydantic Schemas or models that validate and serialize incoming and outgoing data for the Message
from pydantic import BaseModel, ConfigDict, EmailStr
import datetime


class MessageBase(BaseModel):
    sender_name: str
    sender_email: EmailStr
    subject: str
    body: str


class MessageOut(MessageBase):
    id: int
    created_at: datetime.datetime | None

    # Allows Pydantic to read SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)
