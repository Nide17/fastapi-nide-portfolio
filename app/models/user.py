# DB Tables
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=True)
    password_reset_token = Column(String, nullable=True)
    password_reset_expires = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("NOW() AT TIME ZONE 'UTC'"))
