from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "00000000000", "PROM_XYZ")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance >= 0
        assert account.pesel == "00000000000"
        assert account.promo_code == None or account.promo_code[0:5] == "PROM_"

    def test_pesel_too_long(self):
        account = Account("Jane", "Smith", "1432553253254355435")
        assert account.pesel == "Invalid"
    
    def test_pesel_too_short(self):
        account = Account("Jane", "Smith", "14325")
        assert account.pesel == "Invalid"
    
    def test_good_promo(self):
        account = Account("Jane", "Smith", "11111111111", "PROM_XYZ")
        assert account.promo_code == "PROM_XYZ"
    
    def test_bad_promo(self):
        account = Account("Jane", "Smith", "11111111111", "jakis_kodzik")
        assert account.promo_code == "Invalid"