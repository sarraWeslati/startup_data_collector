from typing import List, Optional
from pydantic import BaseModel


class Investor(BaseModel):
    entity_type: str = "investor"
    investor_name: Optional[str] = None
    investor_type: Optional[str] = None
    website: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    investment_sectors: List[str] = []
    total_investments: Optional[int] = None
    source_url: Optional[str] = None
