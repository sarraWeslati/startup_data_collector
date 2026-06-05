from typing import List, Optional
from pydantic import BaseModel


class Startup(BaseModel):
    entity_type: str = "startup"
    startup_name: Optional[str] = None
    sector: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    founding_year: Optional[int] = None
    founders: List[str] = []
    website: Optional[str] = None
    email: Optional[str] = None
    linkedin: Optional[str] = None
    status: Optional[str] = None
    startup_stage: Optional[str] = None
    investors: List[str] = []
    source_url: Optional[str] = None
