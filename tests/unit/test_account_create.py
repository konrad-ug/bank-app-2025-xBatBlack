import pytest

from src.account import Account
from src.account import CompanyAccount
from src.account import PersonalAccount


@pytest.fixture
def personal_account():
    return PersonalAccount("John", "Doe", "12345678901")

@pytest.fixture
def company_account():
    return CompanyAccount("Firma", "1234567890")

class TestAccount:
    def test_account_creation(self, personal_account):
        assert personal_account.first_name == "John"
        assert personal_account.last_name == "Doe"
        assert personal_account.pesel == "12345678901"
        assert personal_account.balance == 0
    
    @pytest.mark.parametrize("pesel, expected", [
        ("12345678901", "12345678901"),  # Poprawny
        ("123", "Invalid"),              # Za krótki
        ("1234567890123456", "Invalid")  # Za długi
    ])

    def test_pesel_validation(self, pesel, expected):
        acc = PersonalAccount("John", "Doe", pesel)
        assert acc.pesel == expected
    
    @pytest.mark.parametrize("pesel, promo_code, expected_code, expected_balance", [
        ("99000000000", "PROM_XYZ", "PROM_XYZ", 50),
        ("61000000000", "PROM_XYZ", "PROM_XYZ", 50),
        ("40000000000", "PROM_XYZ", "Invalid", 0),     # senior nie kwalifikuje się
        ("88000000000", "zly_kod", "Invalid", 0)       # zły kod
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
        assert personal_account.balance == 50  # balans nie powinien się zmienić
    
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
        assert len(personal_account.historia) == 0  # historia nie powinna się zmienić

class TestCompanyAccount:
    @pytest.mark.parametrize("nip, expected", [
        ("1234567890", "1234567890"),  # Poprawny
        ("123", "Invalid"),            # Za krótki
        ("1234567890123", "Invalid")   # Za długi
    ])

    def test_nip(self, nip, expected):
        acc = CompanyAccount("Firma", nip)
        assert acc.nip == expected

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
        assert company_account.balance == 200  # balans nie powinien się zmienić
    
    def test_express_transfer(self, company_account):
        company_account.incoming_transfer(1000)
        company_account.express_transfer(400)
        assert company_account.balance == 595
        assert company_account.historia == [1000, -400, -5]
    
    def test_express_transfer_fail(self, company_account):
        company_account.balance = 300
        company_account.express_transfer(400)
        assert company_account.balance == 300
        assert len(company_account.historia) == 0  # historia nie powinna się zmienić
    
    def test_express_transfer_fee_overdraft(self, company_account):
        company_account.balance = 100
        company_account.express_transfer(100)
        assert company_account.balance == -5
        assert company_account.historia == [-100, -5]
        

class TestLoan:
    @pytest.mark.parametrize("history, loan_amount, expected_result", [
        # Przypadek 1: Ostatnie 3 to wpłaty -> Kredyt tak
        ([100, 100, 100], 500, True),
        ([500, -100, 10, 10, 10], 1000, True), 
        
        # Przypadek 2: Suma ostatnich 5 > kwota -> Kredyt tak
        ([100, 100, 100, 100, 200], 500, True), # Suma = 600 > 500
        ([-100, 200, 200, 200, 200], 600, True), # Suma ost. 5 = 700 > 600
        
        # Przypadki negatywne
        ([100, 100], 500, False),               # Za krótka historia
        ([100, -100, 100, -100, 100], 500, False), # Suma 300 < 500
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
        