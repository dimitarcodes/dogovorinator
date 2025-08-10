import sqlite3
import os
from pathlib import Path

class DogovorinatorDatabase:
    _instance = None

    def __new__(cls, db_path="data/dogovorinator.db"):
        if cls._instance is None:
            cls._instance = super(DogovorinatorDatabase, cls).__new__(cls)
        return cls._instance

    def get_connection(self):
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            DogovorinatorDatabase._instance = None

    def __init__(self, db_path='data/dogovorinator.db'):
        # ensure file path exists
        self.init_database(db_path)
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
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
                name_en TEXT NOT NULL,
                name_bg TEXT NOT NULL,
                bulstat TEXT NOT NULL,
                address_en TEXT NOT NULL,
                address_bg TEXT NOT NULL,
                repr_en TEXT NOT NULL,
                repr_bg TEXT NOT NULL
            )
        ''')
        self.connection.commit()