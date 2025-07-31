from src.database import DogovorinatorDatabase


class CompanyModel:
    def __init__(self, db):
        self.db = db

    def create_example_entry(self, name='ПРИМЕРНА КОМПАНИЯ ЕООД', vat_number='BG123456789', address='София, България'):
        self.insert_company(name=name, vat_number=vat_number, address=address)

    def remove_example_entry(self):
        self.cursor.execute('DELETE FROM companies WHERE name = ?', ('ПРИМЕРНА КОМПАНИЯ ЕООД',))
        self.connection.commit()

    def insert_company(self, name, vat_number, address):
        self.cursor.execute('''
            INSERT INTO companies (name, vat_number, address)
            VALUES (?, ?, ?)
        ''', (name, vat_number, address))
        self.connection.commit()
    
    def fetch_all_companies(self):
        self.cursor.execute('SELECT * FROM companies')
        companies = self.cursor.fetchall()
        return [{'id': row[0], 'name': row[1], 'vat_number': row[2], 'address': row[3]} for row in companies]