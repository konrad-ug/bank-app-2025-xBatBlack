import pytest
from unittest.mock import Mock, patch
from src.mongo_accounts_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount

class TestMongoRepository:
    @patch('src.mongo_accounts_repository.MongoClient')
    def test_save_all(self, mock_client):
        mock_db = mock_client.return_value["bank_db"]
        mock_collection = mock_db["accounts"]
        
        repo = MongoAccountsRepository()
        
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        accounts = [account]

        repo.save_all(accounts)
        
        mock_collection.delete_many.assert_called_once_with({})
        args, _ = mock_collection.insert_many.call_args
        inserted_data = args[0]
        assert len(inserted_data) == 1
        assert inserted_data[0]["pesel"] == "12345678901"
        assert inserted_data[0]["type"] == "personal"

    @patch('src.mongo_accounts_repository.MongoClient')
    def test_load_all(self, mock_client):
        mock_db = mock_client.return_value["bank_db"]
        mock_collection = mock_db["accounts"]
        fake_db_data = [
            {
                "type": "personal",
                "first_name": "Anna",
                "last_name": "Nowak",
                "pesel": "99999999999",
                "promo_code": None,
                "balance": 100,
                "history": [100]
            }
        ]
        mock_collection.find.return_value = fake_db_data
        
        repo = MongoAccountsRepository()
        
        accounts = repo.load_all()
        
        assert len(accounts) == 1
        assert isinstance(accounts[0], PersonalAccount)
        assert accounts[0].first_name == "Anna"
        assert accounts[0].balance == 100