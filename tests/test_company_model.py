# write tests for CompanyModel with pytest
import os
import pytest
from src.db import DogovorinatorDatabase
from src.models.company_model import CompanyModel
from src.models.entities import Company

@pytest.fixture(scope='session')
def company_model():
    db = DogovorinatorDatabase('/data/testbase.db')
    yield CompanyModel(db)
    db.close()
    os.remove('/data/testbase.db')  # Clean up the test database file

def test_create_example_entry(company_model):
    company_model.create_example_entry()
    companies = company_model.get_all_companies()
    assert len(companies) == 1
    assert companies[0].name == 'ПРИМЕРНА КОМПАНИЯ ЕООД'

def test_remove_example_entry(company_model):
    company_model.create_example_entry()
    company_model.remove_example_entry()
    companies = company_model.get_all_companies()
    assert len(companies) == 0

def test_insert_company(company_model):
    company_model.insert_company(Company('Test Company', 'BG987654321', 'Test Address'))
    companies = company_model.get_all_companies()
    assert len(companies) == 1
    assert companies[0].name == 'Test Company'
    assert companies[0].vat_number == 'BG987654321'
    assert companies[0].address == 'Test Address'

def test_remove_company(company_model):
    company_model.insert_company('Test Company', 'BG987654321', 'Test Address')
    companies = company_model.get_all_companies()
    assert len(companies) == 1
    company_model.remove_company(companies[0])
    companies = company_model.get_all_companies()
    assert len(companies) == 0