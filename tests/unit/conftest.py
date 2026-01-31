import pytest
from unittest.mock import patch, Mock
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from src.account_registry import AccountRegistry

@pytest.fixture
def personal_account():
    return PersonalAccount("John", "Doe", "12345678901")

@pytest.fixture
def company_account():
    with patch('src.company_account.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        mock_get.return_value = mock_response
        
        return CompanyAccount("Firma", "1234567890")

@pytest.fixture
def registry():
    return AccountRegistry()