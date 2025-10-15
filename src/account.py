class Account:
    def __init__(self, first_name, last_name, pesel, promo_code = None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        #self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        if self.is_pesel_valid(pesel):
            self.pesel = pesel
        else:
            self.pesel = "Invalid"
        self.promo_code = promo_code
    
    def is_pesel_valid(self, pesel):
        if len(pesel) == 11:
            return True
        return False

    def check_promo(self):
        if self.promo_code[0:5] == "PROM_" and int(self.pesel[0:2]) > 60:
            self.balance += 50