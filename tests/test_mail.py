import pytest
from unittest.mock import patch, Mock
from datetime import date
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestMailHistory:
    @patch('src.personal_account.SMTPClient')
    def test_send_history_personal_success(self, mock_smtp_class):
        mock_smtp_instance = mock_smtp_class.return_value
        mock_smtp_instance.send.return_value = True
        
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.incoming_transfer(100)
        account.outgoing_transfer(50)
        #historia: [100, -50]
        
        today = date.today().strftime('%Y-%m-%d')
        expected_subject = f"Account Transfer History {today}"
        expected_text = "Personal account history: [100, -50]"
        email = "jan@test.com"
        result = account.send_history_via_email(email)

        assert result is True
        mock_smtp_instance.send.assert_called_once_with(expected_subject, expected_text, email)

    @patch('src.personal_account.SMTPClient')
    def test_send_history_personal_fail(self, mock_smtp_class):
        mock_smtp_instance = mock_smtp_class.return_value
        mock_smtp_instance.send.return_value = False 
        
        account = PersonalAccount("Jan", "Kowalski", "12345678901")

        result = account.send_history_via_email("fail@test.com")

        assert result is False

    #konto firmowe
    @patch('src.company_account.requests.get') # Mockujemy API MF (wymóg z Lab 9/10)
    @patch('src.company_account.SMTPClient')   # Mockujemy SMTP w module company_account
    def test_send_history_company_success(self, mock_smtp_class, mock_requests):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}
        mock_requests.return_value = mock_resp

        mock_smtp_instance = mock_smtp_class.return_value
        mock_smtp_instance.send.return_value = True

        company = CompanyAccount("Firma", "1234567890")
        company.incoming_transfer(1000)
        #historia: [1000]

        today = date.today().strftime('%Y-%m-%d')
        expected_subject = f"Account Transfer History {today}"
        expected_text = "Company account history: [1000]"
        email = "firma@test.com"

        result = company.send_history_via_email(email)

        assert result is True
        mock_smtp_instance.send.assert_called_once_with(expected_subject, expected_text, email)