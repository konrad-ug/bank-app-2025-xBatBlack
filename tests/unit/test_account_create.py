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

class TestTransfers:
    def test_incoming_transfer(self):
        account = Account("Alice", "Brown", "22222222222")
        before_balance = account.balance
        account.incoming_transfer(100)
        assert account.balance == before_balance + 100
    
    def test_outgoing_transfer(self):
        account = Account("Walter", "White", "33525333862")
        account.balance = 200
        before_balance = account.balance
        account.outgoing_transfer(100)
        assert account.balance == before_balance - 100
    
    def test_outgoing_transfer_fail(self):
        account = Account("Walter", "White", "33525333862")
        account.balance = 50
        before_balance = account.balance
        account.outgoing_transfer(100)
        assert account.balance == before_balance # balans nie może się zmienić bo za mało pieniędzy na koncie
        