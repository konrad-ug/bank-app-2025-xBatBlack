import pytest
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from src.account_registry import AccountRegistry

@pytest.fixture
def personal_account():
    return PersonalAccount("John", "Doe", "12345678901")

@pytest.fixture
def company_account():
    return CompanyAccount("Firma", "1234567890")

@pytest.fixture
def registry():
    return AccountRegistry()