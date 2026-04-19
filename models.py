from pydantic import BaseModel
from typing import Optional

class LeadPayload(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    message: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_content: Optional[str] = None
    utm_term: Optional[str] = None
    source_tag: Optional[str] = None