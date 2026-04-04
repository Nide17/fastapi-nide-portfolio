# Pydantic Schemas or models that validate and serialize incoming and outgoing data for the Message
from pydantic import BaseModel, ConfigDict
from typing import Optional

class MessageBase(BaseModel):
    sender_name: str
    sender_email: str
    subject: str
    body: str

class MessageOut(MessageBase):
    id: int
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True) # Allows Pydantic to read SQLAlchemy objects
