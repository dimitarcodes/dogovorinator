from dataclasses import dataclass
from typing import Optional

### current company model used as development placeholder
@dataclass
class Company:
    name: str
    vat_number: str
    address: str
    id: Optional[int] = None # database will assign this automatically


### This will be the proper company model to be implemented later
@dataclass
class CompanyProper:
    id: int
    name_bg: str
    name_en: str
    address_bg: str
    address_en: str
    bulstat: str
    ceo_bg: str
    ceo_en: str
