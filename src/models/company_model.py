from src.models.entities import Company
class CompanyModel:
    def __init__(self, db):
        self.db = db
        self.connection = self.db.get_connection()
        self.cursor = self.connection.cursor()

    def create_example_entry(self, company = Company( 
                                                name='ПРИМЕРНА КОМПАНИЯ ЕООД', 
                                                vat_number='BG123456789', 
                                                address='София, България'
                                                )
                                            ):
        self.insert_company(company)

    def remove_example_entry(self):
        self.cursor.execute('DELETE FROM companies WHERE name = ?', 
                            ('ПРИМЕРНА КОМПАНИЯ ЕООД',))
        self.connection.commit()

    def remove_company(self, company: Company):
        self.remove_company_by_id(company.id)

    def remove_company_by_id(self, company_id : int):
        self.cursor.execute('DELETE FROM companies WHERE id = ?',
                            (company_id,))
        self.connection.commit()
        
    def insert_company(self, company: Company): 
        self.cursor.execute('''
            INSERT INTO companies (name, vat_number, address)
            VALUES (?, ?, ?)
        ''', (company.name, company.vat_number, company.address))
        self.connection.commit()
    
    def get_all_companies(self) -> list[Company]:
        self.cursor.execute('SELECT * FROM companies')
        companies_rows = self.cursor.fetchall()
        # return [[{'id': row[0], 'name': row[1], 'vat_number': row[2], 'address': row[3]} for row in companies]]
        return [Company(**row) for row in companies_rows]