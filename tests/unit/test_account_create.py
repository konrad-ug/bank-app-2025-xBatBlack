from src.account import Account
from src.account import CompanyAccount
from src.account import PersonalAccount


class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "00000000000", "PROM_XYZ")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance >= 0
        assert account.pesel == "00000000000"
        assert account.promo_code == None or account.promo_code[0:5] == "PROM_"

    def test_pesel_too_long(self):
        account = PersonalAccount("Jane", "Smith", "1432553253254355435")
        assert account.pesel == "Invalid"
    
    def test_pesel_too_short(self):
        account = PersonalAccount("Jane", "Smith", "14325")
        assert account.pesel == "Invalid"
    
    def test_good_promo(self):
        account = PersonalAccount("Jane", "Smith", "11111111111", "PROM_XYZ")
        assert account.promo_code == "PROM_XYZ"
    
    def test_bad_promo(self):
        account = PersonalAccount("Jane", "Smith", "11111111111", "jakis_kodzik")
        assert account.promo_code == "Invalid"

class TestTransfers:
    def test_incoming_transfer(self):
        account = PersonalAccount("Alice", "Brown", "22222222222")
        before_balance = account.balance
        account.incoming_transfer(100)
        assert account.balance == before_balance + 100
    
    def test_outgoing_transfer(self):
        account = PersonalAccount("Walter", "White", "33525333862")
        account.balance = 200
        before_balance = account.balance
        account.outgoing_transfer(100)
        assert account.balance == before_balance - 100
    
    def test_outgoing_transfer_fail(self):
        account = PersonalAccount("Walter", "White", "33525333862")
        account.balance = 50
        before_balance = account.balance
        account.outgoing_transfer(100)
        assert account.balance == before_balance # balans nie może się zmienić bo za mało pieniędzy na koncie

class TestCompanyAccount:
    def test_nip_too_long(self):
        account = CompanyAccount("jakasfirma", "111111111111")
        assert account.nip == "Invalid"
    
    def test_nip_too_short(self):
        account = CompanyAccount("firma2", "1111")
        assert account.nip == "Invalid"
    
    def test_good_account(self):
        account = CompanyAccount("firma67", "1234567890")
        assert account.nip == "1234567890"
        assert account.name == "firma67"

    def test_incoming_transfer(self):
        account = CompanyAccount("firma3", "1111111111")
        balance1 = account.balance
        account.incoming_transfer(500)
        assert account.balance == balance1 + 500
    
    def test_outgoing_transfer(self):
        account = CompanyAccount("firma61", "2222222222")
        account.balance = 300
        balance1 = account.balance
        account.outgoing_transfer(100)
        assert account.balance == balance1 - 100
        
        
        