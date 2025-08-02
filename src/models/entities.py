from dataclasses import dataclass, fields, field
from typing import Optional

### current company model used as development placeholder
@dataclass
class Company:
    name: str = field(metadata={"label": "Име на фирмата"})
    vat_number: str = field(metadata={"label": "Данъчен номер"})
    address: str = field(metadata={"label": "Адрес"})
    id: Optional[int] = None # database will assign this automatically
    
    @classmethod
    def get_fields(cls):
        return [field.name for field in fields(cls) if field.name != 'id']
@dataclass
class Employee:
    name: str
    pnof: str
    date_of_birth: float
    citizenship: str
    passport_number: str
    id: Optional[int] = None

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

if __name__ == "__main__":
    # get fields:
    for field in fields(Company):
        print(f"{field.name}: {field.type}")