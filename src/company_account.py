import os
import requests
from datetime import date
from src.account import Account
from src.smtp.smtp import SMTPClient

class CompanyAccount(Account):
    def __init__(self, name, nip, balance=0):
        super().__init__()
        self.name = name
        self.express_fee = 5
        self.balance = balance

        if self.is_nip_valid(nip):
            if self._verify_nip_with_mf(nip):
                self.nip = nip
            else:
                raise ValueError("Company not registered!!")
        else:
            self.nip = "Invalid"
        
    def is_nip_valid(self, nip):
        return len(nip) == 10
    
    def _verify_nip_with_mf(self, nip):
        base_url = os.environ.get("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/")
        today = date.today().strftime("%Y-%m-%d")
        endpoint = f"{base_url}api/search/nip/{nip}?date={today}"
        
        try:
            print(f"Sending request to: {endpoint}") 
            response = requests.get(endpoint)
            
            print(f"MF API Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data and "subject" in data["result"]:
                    return data["result"]["subject"]["statusVat"] == "Czynny"
            
            return False
            
        except requests.RequestException as e:
            print(f"API Error: {e}")
            return False
    
    def take_loan(self, amount):
        if self.balance >= amount * 2 and self._check_zus_transfer():
            self.balance += amount
            return True
        return False
    
    def _check_zus_transfer(self):
        return -1775 in self.historia
    
    def send_history_via_email(self, email_address):
        subject = f"Account Transfer History {date.today().strftime('%Y-%m-%d')}"
        text = f"Company account history: {self.historia}"
        
        smtp = SMTPClient()
        return smtp.send(subject, text, email_address)