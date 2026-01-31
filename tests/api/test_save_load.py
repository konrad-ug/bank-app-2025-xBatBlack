import pytest
from app.api import app, registry
from src.personal_account import PersonalAccount

@pytest.fixture
def client():
    app.config['TESTING'] = True
    registry.accounts = []
    with app.test_client() as client:
        yield client

def test_save_and_load_workflow(client):
    account = PersonalAccount("Test", "Mongo", "12345678901")
    registry.add_account(account)

    response_save = client.post("/api/accounts/save")
    assert response_save.status_code == 200
    assert response_save.json["message"] == "Accounts saved"

    registry.accounts = []
    assert registry.get_count() == 0

    response_load = client.post("/api/accounts/load")
    assert response_load.status_code == 200
    
    assert registry.get_count() == 1
    loaded_account = registry.get_account_by_pesel("12345678901")
    assert loaded_account is not None
    assert loaded_account.first_name == "Test"
    assert loaded_account.last_name == "Mongo"