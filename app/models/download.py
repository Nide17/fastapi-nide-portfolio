# DB Tables
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.db.session import Base


class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip_address = Column(String, nullable=False)
    document_name = Column(String, nullable=False)
    device = Column(String, nullable=True)
    # Can be extracted from the user agent string
    operating_system = Column(String, nullable=True)
    # Can be extracted from the user agent string
    browser = Column(String, nullable=True)
    # Can be extracted from the IP address using a geolocation service
    country = Column(String, nullable=True)
    # Can be extracted from the user agent string or the request headers
    referrer = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text("(NOW() AT TIME ZONE 'UTC')"))
