from datetime import date
from src.smtp.smtp import SMTPClient
from src.account import Account

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
    
    def submit_for_loan(self, amount):
        if self._check_last_3_transactions_positive() or self._check_sum_last_5_transactions(amount):
            self.balance += amount
            return True
        return False
    
    def _check_last_3_transactions_positive(self):
        if len(self.historia) < 3:
            return False
        return all(t > 0 for t in self.historia[-3:])

    def _check_sum_last_5_transactions(self, loan_amount):
        if len(self.historia) < 5:
            return False
        return sum(self.historia[-5:]) > loan_amount
    
    def send_history_via_email(self, email_address):
        subject = f"Account Transfer History {date.today().strftime('%Y-%m-%d')}"
        text = f"Personal account history: {self.historia}"
        
        smtp = SMTPClient()
        return smtp.send(subject, text, email_address)
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type" : "personal",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "pesel": self.pesel,
            "promo_code": 'promo_code'
        })
        return data