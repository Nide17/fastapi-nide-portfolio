# DB Tables
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    # Store hashed passwords, never store plain text passwords
    password_hash = Column(String, nullable=False)
    # Can be used for admin or regular user roles
    role = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
