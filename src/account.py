class Account:
    def __init__(self):
        self.balance = 0
        self.historia = []
    
    def incoming_transfer(self, amount):
        self.balance += amount
        self.historia.append(amount)
        return True

    def outgoing_transfer(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.historia.append(-amount)
            return True
        else:
            return False
    
    def express_transfer(self, amount):
        if self.balance >= amount:
            self.balance -= (amount + self.express_fee)
            self.historia.append(-amount)
            self.historia.append(-self.express_fee)
            return True
        else:
            return False