from src.models.entities import Company
from src.logger import DogovLogger

log = DogovLogger.get_logger()

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
            INSERT INTO companies (name, vat_number, address)
            VALUES (?, ?, ?)
        ''', (company.name, company.vat_number, company.address))
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
            SET name = ?, vat_number = ?, address = ?
            WHERE id = ?
        ''', (company.name, company.vat_number, company.address, company.id))
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