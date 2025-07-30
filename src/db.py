import sqlite3
import os
from pathlib import Path

class DogovorinatorDatabase:
    def __init__(self, db_name='data/dogovorinator.db'):
        # ensure file path exists
        self.init_database(db_name)
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.init_tables()

    def init_database(self, db_path):
        # Ensure the database directory exists
        db_dir = Path(db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

    def init_tables(self):
        # Create necessary tables if they do not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                vat_number TEXT NOT NULL,
                address TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def insert_example_entry(self, name='ПРИМЕРНА КОМПАНИЯ ЕООД', vat_number='BG123456789', address='София, България'):
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

    def close(self):
        self.connection.close()