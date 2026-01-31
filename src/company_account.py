from src.account import Account

class CompanyAccount(Account):
    def __init__(self, name, nip, balance=0):
        super().__init__()
        self.name = name
        self.express_fee = 5
        #self.nip = nip if self.is_nip_valid(nip) else "Invalid

        if self.is_nip_valid(nip):
            self.nip = nip
        else:
            self.nip = "Invalid"
        self.balance = balance
        
    def is_nip_valid(self, nip):
        return len(nip) == 10
    
    def take_loan(self, amount):
        if self.balance >= amount * 2 and self._check_zus_transfer():
            self.balance += amount
            return True
        return False
    
    def _check_zus_transfer(self):
        return -1775 in self.historia