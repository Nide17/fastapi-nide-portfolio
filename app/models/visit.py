# DB Tables
from sqlalchemy import Column, Integer, String, DateTime
from app.db.session import Base

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, nullable=False)
    device = Column(String, nullable=True)
    operating_system = Column(String, nullable=True) # Can be extracted from the user agent string
    browser = Column(String, nullable=True) # Can be extracted from the user agent string
    country = Column(String, nullable=True) # Can be extracted from the IP address using a geolocation service
    path = Column(String, nullable=True) # The path of the visited page, can be extracted from the request URL
    referrer = Column(String, nullable=True)
    created_at = Column(DateTime)
    