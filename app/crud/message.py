# This separates DB queries from API logic (routes)
from sqlalchemy.orm import Session
from app.models.message import Message

def get_all_messages(db: Session):
    """Fetches all messages from the database."""
    return db.query(Message).all()

def get_message_by_id(db: Session, message_id: int):
    """Fetches a single message by its ID."""
    return db.query(Message).filter(Message.id == message_id).first()

def add_message(db: Session, message_data):
    """Creates a new message in the database."""
    new_message = Message(**message_data.model_dump())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message
