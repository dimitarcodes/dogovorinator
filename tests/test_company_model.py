# write tests for CompanyModel with pytest
import os
import pytest
from src.db import DogovorinatorDatabase
from src.models.company_model import CompanyModel
from src.models.company_model import Company
import tempfile, shutil

@pytest.fixture(scope='session')
def company_model():
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, 'test.db')
    db = DogovorinatorDatabase(db_path)
    yield CompanyModel(db)
    db.close()
    try:
        shutil.rmtree(temp_dir)  # Clean up the test database file
    except FileNotFoundError:
        pass

def test_add_company(company_model):
    """
    Test inserting a company.
    Successful insertion should return the company with an id.
    The original company instance should be augmented with the id.
    """
    example_company = Company(
        name='Test Company',
        vat_number='BG987654321',
        address='Test Address'
    )
    added_company = company_model.add_company(example_company)
    assert added_company.id is not None
    assert added_company.id == example_company.id
    assert added_company.name == 'Test Company'

def test_get_companies(company_model):
    example_company = Company(
        name='Test Company',
        vat_number='BG987654321',
        address='Test Address'
    )
    company_model.add_company(example_company)
    companies = company_model.get_companies()
    assert len(companies) > 0
    assert companies[0].name == 'Test Company'

def test_remove_company(company_model):
    """
    Test removing a company.
    """
    example_company = Company(
        name='Test Company',
        vat_number='BG987654321',
        address='Test Address'
    )
    company_model.add_company(example_company)
    n_companies = len(company_model.get_companies())
    company_model.remove_company(example_company)
    new_n_companies = len(company_model.get_companies())
    assert new_n_companies == n_companies - 1