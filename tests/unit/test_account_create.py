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

class TestPersonalAccountTransfers:
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
    
    def test_express_transfer_valid(self):
        account = PersonalAccount("Bob", "Marley", "44556677889")
        account.balance = 300
        before_balance = account.balance
        account.express_transfer(100)
        assert account.balance == before_balance - (100 + account.express_fee)  # 100 + 1 express fee
    
    def test_express_transfer_invalid(self):
        account = PersonalAccount("Bob", "Marley", "44566677889")
        account.balance = 300
        before_balance = account.balance
        result = account.express_transfer(400)  # więcej niż na koncie
        assert result == False
        assert account.balance == before_balance  # balans nie może się zmienić
    
    def test_express_transfer_exact(self):
        account = PersonalAccount("Frank", "Jonas", "44599677889")
        account.balance = 300  # dokładnie tyle, żeby pokryć kwotę + opłatę
        before_balance = account.balance
        account.express_transfer(300)
        assert account.balance == before_balance - (300 + account.express_fee)  # 300 + 1 express fee

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
    
    def test_express_transfer_valid(self):
        account = CompanyAccount("firmaExpress", "3333333333")
        account.balance = 500
        balance1 = account.balance
        account.express_transfer(100)
        assert account.balance == balance1 - (100 + account.express_fee)  # 100 + 5 express fee
    
    def test_express_transfer_invalid(self):
        account = CompanyAccount("firmaExpress2", "4444444444")
        account.balance = 500
        balance1 = account.balance
        result = account.express_transfer(600)  # więcej niż na koncie
        assert result == False
        assert account.balance == balance1  # balans nie może się zmienić
    
    def test_express_transfer_exact(self):
        account = CompanyAccount("firmaExpress3", "5555555555")
        account.balance = 500  # dokładnie tyle, żeby pokryć kwotę + opłatę
        balance1 = account.balance
        account.express_transfer(500)
        assert account.balance == balance1 - (500 + account.express_fee)  # 500 + 5 express fee
        

class TestTransferHistory:
    def test_transfer_history_personal(self):
        account = PersonalAccount("Test", "User", "12345678901")
        account.incoming_transfer(200)
        account.outgoing_transfer(50)
        account.express_transfer(30)
        expected_history = [200, -50, -30, -account.express_fee]
        assert account.historia == expected_history

    def test_transfer_history_company(self):
        account = CompanyAccount("TestCo", "9876543210")
        account.incoming_transfer(500)
        account.outgoing_transfer(150)
        account.express_transfer(100)
        expected_history = [500, -150, -100, -account.express_fee]
        assert account.historia == expected_history
        