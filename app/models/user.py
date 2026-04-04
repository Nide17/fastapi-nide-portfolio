# DB Tables
from sqlalchemy import Column, Integer, String, DateTime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False) # Store hashed passwords, never store plain text passwords
    role = Column(String, nullable=True) # Can be used for admin or regular user roles
    created_at = Column(DateTime)
