# DB Tables
from sqlalchemy import Column, Integer, String, DateTime
from app.db.session import Base

class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, nullable=False)
    document_name = Column(String, nullable=False)
    device = Column(String, nullable=True)
    operating_system = Column(String, nullable=True) # Can be extracted from the user agent string
    browser = Column(String, nullable=True) # Can be extracted from the user agent string
    country = Column(String, nullable=True) # Can be extracted from the IP address using a geolocation service
    referrer = Column(String, nullable=True) # Can be extracted from the user agent string or the request headers
    created_at = Column(DateTime)
