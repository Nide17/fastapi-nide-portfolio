# Pydantic Schemas or models that validate and serialize incoming and outgoing data for the Download
from pydantic import BaseModel, ConfigDict
from typing import Optional

class DownloadBase(BaseModel):
    ip_address: str
    document_name: str
    device: Optional[str] = None
    operating_system: Optional[str] = None # Can be extracted from the user agent string
    browser: Optional[str] = None # Can be extracted from the user agent string
    country: Optional[str] = None # Can be extracted from the IP address using a geolocation service
    referrer: Optional[str] = None # Can be extracted from the user agent string or the request headers

class DownloadOut(DownloadBase):
    id: int
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True) # Allows Pydantic to read SQLAlchemy objects
