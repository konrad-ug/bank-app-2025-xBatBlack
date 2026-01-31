class AccountRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        if hasattr(account, 'pesel'):
            existing_account = self.get_account_by_pesel(account.pesel)
            if existing_account:
                return False
        
        self.accounts.append(account)
        return True

    def get_count(self):
        return len(self.accounts)

    def get_account_by_pesel(self, pesel):
        for account in self.accounts:
            if hasattr(account, 'pesel') and account.pesel == pesel:
                return account
        return None
        
    def get_all_accounts(self):
        return self.accounts
    
    def delete_account(self, pesel):
        account = self.get_account_by_pesel(pesel)
        if account:
            self.accounts.remove(account)
            return True
        return False