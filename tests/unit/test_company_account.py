import pytest
from unittest.mock import patch, Mock
from src.company_account import CompanyAccount

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


class TestCompanyAccountCreation:
    @patch('src.company_account.requests.get')
    def test_create_verified_company(self, mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {"statusVat": "Czynny", "name": "Firma Testowa"}
            }
        }
        mock_get.return_value = mock_response
        acc = CompanyAccount("Firma", "1234567890")
        assert acc.nip == "1234567890"
        assert mock_get.called

    #Poprawny NIP, ale firma nie istnieje lub nie jest "Czynna"
    @patch('src.company_account.requests.get')
    def test_create_unverified_company_raises_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "subject": {"statusVat": "Zwolniony"}
            }
        }
        mock_get.return_value = mock_response
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Firma", "1234567890")

    #Błąd API
    @patch('src.company_account.requests.get')
    def test_create_company_api_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Firma", "1234567890")

    #Niepoprawna długość NIP
    @patch('src.company_account.requests.get')
    @pytest.mark.parametrize("nip", ["123", "1234567890123"])
    def test_invalid_nip_length(self, mock_get, nip):
        acc = CompanyAccount("Firma", nip)
        assert acc.nip == "Invalid"
        assert not mock_get.called

class TestCompanyAccountTransfers:
    def test_incoming_transfer(self, company_account):
        company_account.incoming_transfer(500)
        assert company_account.balance == 500
        assert company_account.historia == [500]
    
    def test_outgoing_transfer_success(self, company_account):
        company_account.incoming_transfer(800)
        company_account.outgoing_transfer(300)
        assert company_account.balance == 500
        assert company_account.historia == [800, -300]
    
    def test_outgoing_transfer_fail(self, company_account):
        company_account.balance = 200
        company_account.outgoing_transfer(400)
        assert company_account.balance == 200
    
    def test_express_transfer(self, company_account):
        company_account.incoming_transfer(1000)
        company_account.express_transfer(400)
        assert company_account.balance == 595
        assert company_account.historia == [1000, -400, -5]
    
    def test_express_transfer_fail(self, company_account):
        company_account.balance = 300
        company_account.express_transfer(400)
        assert company_account.balance == 300
        assert len(company_account.historia) == 0
    
    def test_express_transfer_fee_overdraft(self, company_account):
        company_account.balance = 100
        company_account.express_transfer(100)
        assert company_account.balance == -5
        assert company_account.historia == [-100, -5]

class TestCompanyAccountLoan:
    @pytest.mark.parametrize("balance, history, loan_amount, expected_result", [
        (2000, [-1775, -100], 1000, True), 
        (5000, [-500, -1775], 2000, True),
        (5000, [-100, -200], 1000, False),
        (1900, [-1775], 1000, False),
        (100, [-50], 1000, False)
    ])
    def test_take_loan(self, company_account, balance, history, loan_amount, expected_result):
        company_account.balance = balance
        company_account.historia = history.copy()
        result = company_account.take_loan(loan_amount)
        assert result == expected_result
        if expected_result:
            assert company_account.balance == balance + loan_amount
        else:
            assert company_account.balance == balance