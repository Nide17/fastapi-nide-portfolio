# Pydantic Schemas or models that validate and serialize incoming and outgoing data for the Download
from pydantic import BaseModel, ConfigDict
from typing import Optional
import datetime


class DownloadBase(BaseModel):
    ip_address: str
    document_name: str
    device: Optional[str] = None
    # Can be extracted from the user agent string
    operating_system: Optional[str] = None
    # Can be extracted from the user agent string
    browser: Optional[str] = None
    # Can be extracted from the IP address using a geolocation service
    country: Optional[str] = None
    # Can be extracted from the user agent string or the request headers
    referrer: Optional[str] = None


class DownloadOut(DownloadBase):
    id: int
    created_at: datetime.datetime | None

    # Allows Pydantic to read SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)
