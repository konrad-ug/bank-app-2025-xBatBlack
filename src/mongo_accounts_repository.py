from pymongo import MongoClient
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
import os

class MongoAccountsRepository:
    def __init__(self):
        host = os.environ.get("MONGO_HOST", "localhost") 
        self.client = MongoClient(f"mongodb://{host}:27017/")
        self.db = self.client["bank_db"]
        self.collection = self.db["accounts"]

    def save_all(self, accounts):
        #czyszczenie kolekcji
        self.collection.delete_many({})
        
        if not accounts:
            return
            
        data_to_insert = [account.to_dict() for account in accounts]
        self.collection.insert_many(data_to_insert)

    def load_all(self):
        documents = self.collection.find({})
        accounts = []
        
        for doc in documents:
            if doc["type"] == "personal":
                acc = PersonalAccount(doc["first_name"], doc["last_name"], doc["pesel"], doc["promo_code"])
                acc.balance = doc["balance"]
                acc.historia = doc["history"]
                accounts.append(acc)
                
            elif doc["type"] == "company":
                acc = CompanyAccount(doc["name"], doc["nip"])
                acc.balance = doc["balance"]
                acc.historia = doc["history"]
                accounts.append(acc)
                
        return accounts