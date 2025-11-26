class Account:
    def __init__(self):
        self.balance = 0
    
    def incoming_transfer(self, amount):
        self.balance += amount

    def outgoing_transfer(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            return False
    
    def express_transfer(self, amount):
        if self.balance >= amount:
            self.balance -= (amount + self.express_fee)
        else:
            return False
    def nieprzetestowana_metoda(self):
        return "Brak testu!"

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code = None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.express_fee = 1
        #self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        if self.is_pesel_valid(pesel):
            self.pesel = pesel
        else:
            self.pesel = "Invalid"
        if promo_code is not None:
            self.check_promo(promo_code)
    
    def is_pesel_valid(self, pesel):
        if len(pesel) == 11:
            return True
        return False

    def check_promo(self, promo_code):
        if promo_code[0:5] == "PROM_" and (int(self.pesel[0:2]) > 60 or int(self.pesel[0:2]) < 24):
            self.balance += 50
            self.promo_code = promo_code
        else:
            self.promo_code = "Invalid"



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