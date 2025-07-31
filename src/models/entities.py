from dataclasses import dataclass

### current company model used as development placeholder
@dataclass
class Company:
    id: int
    name: str
    vat_number: str
    address: str


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
