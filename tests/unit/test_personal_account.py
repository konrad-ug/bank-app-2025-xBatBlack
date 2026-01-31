import pytest
from src.personal_account import PersonalAccount

class TestPersonalAccount:
    def test_creation(self, personal_account):
        assert personal_account.first_name == "John"
        assert personal_account.last_name == "Doe"
        assert personal_account.pesel == "12345678901"
        assert personal_account.balance == 0
    
    @pytest.mark.parametrize("pesel, expected", [
        ("12345678901", "12345678901"),
        ("123", "Invalid"),
        ("1234567890123456", "Invalid")
    ])
    def test_pesel_validation(self, pesel, expected):
        acc = PersonalAccount("John", "Doe", pesel)
        assert acc.pesel == expected
    
    @pytest.mark.parametrize("pesel, promo_code, expected_code, expected_balance", [
        ("99000000000", "PROM_XYZ", "PROM_XYZ", 50),
        ("61000000000", "PROM_XYZ", "PROM_XYZ", 50),
        ("40000000000", "PROM_XYZ", "Invalid", 0),
        ("88000000000", "zly_kod", "Invalid", 0)
    ])
    def test_promo_codes(self, pesel, promo_code, expected_code, expected_balance):
        acc = PersonalAccount("John", "Doe", pesel, promo_code)
        assert acc.promo_code == expected_code
        assert acc.balance == expected_balance

class TestPersonalAccountTransfers:
    def test_incoming_transfer(self, personal_account):
        personal_account.incoming_transfer(100)
        assert personal_account.balance == 100
        assert personal_account.historia == [100]
    
    def test_outgoing_transfer_success(self, personal_account):
        personal_account.incoming_transfer(200)
        personal_account.outgoing_transfer(100)
        assert personal_account.balance == 100
        assert personal_account.historia == [200, -100]
    
    def test_outgoing_transfer_fail(self, personal_account):
        personal_account.balance = 50
        personal_account.outgoing_transfer(100)
        assert personal_account.balance == 50
    
    def test_express_transfer(self, personal_account):
        personal_account.incoming_transfer(300)
        personal_account.express_transfer(100)
        assert personal_account.balance == 199
        assert personal_account.historia == [300, -100, -1]
    
    def test_express_transfer_exact(self, personal_account):
        personal_account.balance = 100
        personal_account.express_transfer(100)
        assert personal_account.balance == -1
        assert personal_account.historia == [-100, -1]

    def test_express_transfer_fail(self, personal_account):
        personal_account.balance = 99
        personal_account.express_transfer(100)
        assert personal_account.balance == 99
        assert len(personal_account.historia) == 0

class TestPersonalLoan:
    @pytest.mark.parametrize("history, loan_amount, expected_result", [
        ([100, 100, 100], 500, True),
        ([500, -100, 10, 10, 10], 1000, True), 
        ([100, 100, 100, 100, 200], 500, True),
        ([-100, 200, 200, 200, 200], 600, True),
        ([100, 100], 500, False),
        ([100, -100, 100, -100, 100], 500, False),
    ])
    def test_loan(self, personal_account, history, loan_amount, expected_result):
        for amount in history:
            if amount > 0:
                personal_account.incoming_transfer(amount)
            else:
                personal_account.historia.append(amount)
                personal_account.balance += amount
        
        initial_balance = personal_account.balance
        result = personal_account.submit_for_loan(loan_amount)
        
        assert result == expected_result
        if result:
            assert personal_account.balance == initial_balance + loan_amount
        else:
            assert personal_account.balance == initial_balance