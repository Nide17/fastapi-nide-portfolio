# DB Tables
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.db.session import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sender_name = Column(String, nullable=False)
    sender_email = Column(String, index=True, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("(NOW() AT TIME ZONE 'UTC')"))
