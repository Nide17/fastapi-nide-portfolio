# Pydantic Schemas or models that validate and serialize incoming and outgoing data for the Visit
from pydantic import BaseModel, ConfigDict
from typing import Optional
import datetime


class VisitBase(BaseModel):
    ip_address: str
    device: Optional[str] = None
    # Can be extracted from the user agent string
    operating_system: Optional[str] = None
    # Can be extracted from the user agent string
    browser: Optional[str] = None
    # Can be extracted from the IP address using a geolocation service
    country: Optional[str] = None
    # The path of the visited page, can be extracted from the request URL
    path: Optional[str] = None
    # Can be extracted from the user agent string or the request headers
    referrer: Optional[str] = None


class VisitOut(VisitBase):
    id: int
    created_at: datetime.datetime | None

    # Allows Pydantic to read SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)
