import pytest
from unittest.mock import Mock, patch
from src.mongo_accounts_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestMongoRepository:
    @patch('src.mongo_accounts_repository.MongoClient')
    def test_save_all_personal(self, mock_client):
        mock_db = mock_client.return_value["bank_db"]
        mock_collection = mock_db["accounts"]
        repo = MongoAccountsRepository()
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        
        repo.save_all([account])
        
        mock_collection.delete_many.assert_called_once_with({})
        args, _ = mock_collection.insert_many.call_args
        inserted_data = args[0]
        assert len(inserted_data) == 1
        assert inserted_data[0]["pesel"] == "12345678901"
        assert inserted_data[0]["type"] == "personal"

    @patch('src.mongo_accounts_repository.MongoClient')
    def test_save_all_empty(self, mock_client):
        mock_db = mock_client.return_value["bank_db"]
        mock_collection = mock_db["accounts"]
        repo = MongoAccountsRepository()
        
        repo.save_all([])
        
        mock_collection.delete_many.assert_called_once_with({}) 
        mock_collection.insert_many.assert_not_called()        

    @patch('src.mongo_accounts_repository.MongoClient')
    def test_load_all_personal(self, mock_client):
        mock_db = mock_client.return_value["bank_db"]
        mock_collection = mock_db["accounts"]
        fake_db_data = [{
            "type": "personal", "first_name": "Anna", "last_name": "Nowak",
            "pesel": "99999999999", "promo_code": None, "balance": 100, "history": [100]
        }]
        mock_collection.find.return_value = fake_db_data
        repo = MongoAccountsRepository()
        
        accounts = repo.load_all()
        
        assert len(accounts) == 1
        assert isinstance(accounts[0], PersonalAccount)
        assert accounts[0].first_name == "Anna"
        assert accounts[0].balance == 100

    @patch('src.company_account.requests.get') 
    @patch('src.mongo_accounts_repository.MongoClient')
    def test_load_all_company(self, mock_client, mock_requests):
        mock_db = mock_client.return_value["bank_db"]
        mock_collection = mock_db["accounts"]
        fake_db_data = [{
            "type": "company", "name": "Januszex", "nip": "8888888888",
            "balance": 5000, "history": [1000, 4000]
        }]
        mock_collection.find.return_value = fake_db_data

        mock_mf_response = Mock()
        mock_mf_response.status_code = 200
        mock_mf_response.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }
        mock_requests.return_value = mock_mf_response

        repo = MongoAccountsRepository()
        
        # Act
        accounts = repo.load_all()
        
        # Assert
        assert len(accounts) == 1
        assert isinstance(accounts[0], CompanyAccount)
        assert accounts[0].name == "Januszex"
        assert accounts[0].balance == 5000
        assert accounts[0].nip == "8888888888"