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
    legal_name: Optional[str] = None
    tagline: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    leadership_team: List[str] = []
    employee_count: Optional[str] = None
    technologies: List[str] = []
    products_services: List[str] = []
    partners: List[str] = []
    customers: List[str] = []
    accelerators: List[str] = []
    incubators: List[str] = []
    awards: List[str] = []
    funding_stage: Optional[str] = None
    funding_amount: Optional[str] = None
    hiring: Optional[bool] = None
    open_positions: List[str] = []
    social_links: dict = {}
    confidence_score: Optional[float] = None
