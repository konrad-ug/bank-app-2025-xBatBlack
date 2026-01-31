import pytest
from app.api import app, registry

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_registry():
    registry.accounts = []

def test_create_account(client):
    payload = {"name": "James", "surname": "Hetfield", "pesel": "12345678901"}
    response = client.post("/api/accounts", json=payload)
    
    assert response.status_code == 201
    assert response.json["message"] == "Account created"
    assert registry.get_count() == 1

def test_create_duplicate_account(client):
    payload = {"name": "James", "surname": "Hetfield", "pesel": "12345678901"}
    client.post("/api/accounts", json=payload)

    response = client.post("/api/accounts", json=payload)
    assert response.status_code == 409
    assert response.json["message"] == "Account with this pesel already exists"

def test_get_all_accounts(client):
    client.post("/api/accounts", json={"name": "A", "surname": "B", "pesel": "11111111111"})
    
    response = client.get("/api/accounts")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]["pesel"] == "11111111111"

def test_get_account_count(client):
    client.post("/api/accounts", json={"name": "A", "surname": "B", "pesel": "11111111111"})
    client.post("/api/accounts", json={"name": "C", "surname": "D", "pesel": "22222222222"})
    
    response = client.get("/api/accounts/count")
    assert response.status_code == 200
    assert response.json["count"] == 2

def test_get_account_by_pesel(client):
    payload = {"name": "Lars", "surname": "Ulrich", "pesel": "99999999999"}
    client.post("/api/accounts", json=payload)
    
    response = client.get("/api/accounts/99999999999")
    assert response.status_code == 200
    assert response.json["surname"] == "Ulrich"
    assert response.json["balance"] == 0

def test_get_account_not_found(client):
    response = client.get("/api/accounts/00000000000")
    assert response.status_code == 404

def test_update_account(client):
    client.post("/api/accounts", json={"name": "Kirk", "surname": "Hammett", "pesel": "88888888888"})
    
    #zmiana imienia
    update_payload = {"name": "Robert"}
    response = client.patch("/api/accounts/88888888888", json=update_payload)
    
    assert response.status_code == 200
    assert response.json["message"] == "Account updated"
    
    #weryfikacja
    acc = registry.get_account_by_pesel("88888888888")
    assert acc.first_name == "Robert"
    assert acc.last_name == "Hammett"

def test_delete_account(client):
    client.post("/api/accounts", json={"name": "Cliff", "surname": "Burton", "pesel": "77777777777"})
    
    response = client.delete("/api/accounts/77777777777")
    assert response.status_code == 200
    assert response.json["message"] == "Account deleted"
    
    assert registry.get_count() == 0
    
    response_retry = client.delete("/api/accounts/77777777777")
    assert response_retry.status_code == 404


#przelewy:

@pytest.fixture
def account_with_funds(client): #fixture z kontem z 1000 zł
    pesel = "99999999999"
    client.post("/api/accounts", json={"name": "Rich", "surname": "Guy", "pesel": pesel})
    client.post(f"/api/accounts/{pesel}/transfer", json={"amount": 1000, "type": "incoming"})
    return pesel

def test_transfer_incoming(client):
    pesel = "11111111111"
    client.post("/api/accounts", json={"name": "Test", "surname": "User", "pesel": pesel})
    response = client.post(f"/api/accounts/{pesel}/transfer", json={"amount": 500, "type": "incoming"})
    assert response.status_code == 200

    acc_res = client.get(f"/api/accounts/{pesel}")
    assert acc_res.json["balance"] == 500

def test_transfer_outgoing_success(client, account_with_funds):
    pesel = account_with_funds
    
    response = client.post(f"/api/accounts/{pesel}/transfer", json={"amount": 200, "type": "outgoing"})
    assert response.status_code == 200
    
    acc_res = client.get(f"/api/accounts/{pesel}")
    assert acc_res.json["balance"] == 800

def test_transfer_outgoing_fail_insufficient_funds(client, account_with_funds):
    pesel = account_with_funds
    
    response = client.post(f"/api/accounts/{pesel}/transfer", json={"amount": 2000, "type": "outgoing"})
    assert response.status_code == 422
    assert response.json["message"] == "Insufficient funds"

def test_transfer_express_success(client, account_with_funds):
    pesel = account_with_funds
    
    response = client.post(f"/api/accounts/{pesel}/transfer", json={"amount": 100, "type": "express"})
    assert response.status_code == 200
    
    acc_res = client.get(f"/api/accounts/{pesel}")
    assert acc_res.json["balance"] == 899

def test_transfer_account_not_found(client): #nieistniejące konto
    response = client.post("/api/accounts/00000000000/transfer", json={"amount": 100, "type": "incoming"})
    assert response.status_code == 404

def test_transfer_invalid_type(client, account_with_funds):
    pesel = account_with_funds
    response = client.post(f"/api/accounts/{pesel}/transfer", json={"amount": 100, "type": "cos_tam"})
    assert response.status_code == 400