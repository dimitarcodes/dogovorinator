from dataclasses import dataclass, fields, field
from typing import Optional

from src.logger import DogovLogger
log = DogovLogger.get_logger()

@dataclass
class Company:
    name_en: str = field(metadata={"label": "Име на фирмата (EN)", "docvar": "CMP_NAME_EN"})
    name_bg: str = field(metadata={"label": "Име на фирмата (БГ)", "docvar": "CMP_NAME_BG"})
    bulstat: str = field(metadata={"label": "БУЛСТАТ", "docvar": "CMP_BULSTAT"})
    address_en: str = field(metadata={"label": "Адрес (EN)", "docvar": "CMP_ADDR_EN"})
    address_bg: str = field(metadata={"label": "Адрес (БГ)", "docvar": "CMP_ADDR_BG"})
    repr_en: str = field(metadata={"label": "Представляващо лице на фирмата (EN)", "docvar": "CMP_REPR_EN"})
    repr_bg: str = field(metadata={"label": "Представляващо лице на фирмата (БГ)", "docvar": "CMP_REPR_BG"})
    id: Optional[int] = None # database will assign this automatically
    
    @classmethod
    def get_fields(cls) -> list[str]:
        return [field.name for field in fields(cls) if field.name != 'id']
    @classmethod
    def get_fields_with_labels(cls) -> dict[str, str]:
        return {field.name: field.metadata["label"] for field in fields(cls) if field.name != 'id'}
    @classmethod
    def get_docvars(cls) -> dict[str, str]:
        return {field.name: field.metadata["docvar"] for field in fields(cls) if field.name != 'id'}


class CompanyModel:
    def __init__(self, db):
        self.db = db
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()

    def remove_company(self, company: Company):
        """ Remove a company by its instance.
        Removals work by id, so if no id is provided an exception will be raised.
        """
        # assert there is an id
        if company.id is None:
            raise ValueError("Company must have an id to be removed.")
        # remove by id
        self.cursor.execute('DELETE FROM companies WHERE id = ?', (company.id,))
        self.connection.commit()
        
    def add_company(self, company: Company) -> Company: 
        self.cursor.execute('''
            INSERT INTO companies (name_en, name_bg, bulstat, address_en, address_bg, repr_en, repr_bg)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (company.name_en, company.name_bg, company.bulstat, company.address_en, company.address_bg, company.repr_en, company.repr_bg))
        self.connection.commit()

        # Get the last inserted id
        company.id = self.cursor.lastrowid
        # Note: this augments the original company instance with the id
        # returning is not necessary but is done for convenience
        return company

    def edit_company(self, company: Company) -> Company:
        """ Edit an existing company in the database. """
        if company.id is None:
            raise ValueError("Company must have an id to be edited.")
        
        self.cursor.execute('''
            UPDATE companies
            SET name_en = ?, name_bg = ?, bulstat = ?, address_en = ?, address_bg = ?, repr_en = ?, repr_bg = ?
            WHERE id = ?
        ''', (company.name_en, company.name_bg, company.bulstat, company.address_en, company.address_bg, company.repr_en, company.repr_bg, company.id))
        self.connection.commit()
        
        return company

    def get_companies(self) -> list[Company]:
        self.cursor.execute('SELECT * FROM companies')
        companies_rows = self.cursor.fetchall()
        return [Company(**row) for row in companies_rows]
    
    @property
    def selected_company(self) -> Company:
        return self._selected_company

    @selected_company.setter
    def selected_company(self, company: Company):
        self._selected_company = company