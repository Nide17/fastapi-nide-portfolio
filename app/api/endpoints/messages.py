# Routes for handling message-related API endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import message as crud_message
from app.schemas.message import MessageBase, MessageOut

router = APIRouter()

@router.get("/", response_model=list[MessageOut])
def read_messages(db: Session = Depends(get_db)):
    """Endpoint to fetch all messages."""
    messages = crud_message.get_all_messages(db)
    return messages

@router.get("/{message_id}", response_model=MessageOut)
def read_message(message_id: int, db: Session = Depends(get_db)):
    """Endpoint to fetch a specific message by its ID."""
    message = crud_message.get_message_by_id(db, message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.post("/", response_model=MessageOut)
def create_message(message_data: MessageBase, db: Session = Depends(get_db)):
    """Endpoint to create a new message."""
    message = crud_message.add_message(db, message_data)
    return message

@router.put("/{message_id}", response_model=MessageOut)
def update_message(message_id: int, message_data: MessageBase, db: Session = Depends(get_db)):
    """Endpoint to update an existing message."""
    existing_message = crud_message.get_message_by_id(db, message_id)
    if existing_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    updated_message = crud_message.edit_message(db, message_id, message_data)
    return updated_message
