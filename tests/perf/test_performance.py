import pytest
import time
from app.api import app, registry

@pytest.fixture
def client(): #dzięki temy nie muszę uruchamiać serwera w tle
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_registry():
    registry.accounts = []

class TestPerformance:
    
    def test_perf_create_delete_account(self, client):
        iterations = 100
        
        for i in range(iterations):
            pesel = f"99{i:09d}" 
            payload = {
                "name": "Perf", 
                "surname": "Test", 
                "pesel": pesel
            }
            start_time = time.time()
            response_create = client.post("/api/accounts", json=payload)
            end_time = time.time()
            
            assert response_create.status_code == 201
            assert (end_time - start_time) < 0.5, f"Create account took too long: {end_time - start_time}s"
            
            start_time = time.time()
            response_delete = client.delete(f"/api/accounts/{pesel}")
            end_time = time.time()
            
            assert response_delete.status_code == 200
            assert (end_time - start_time) < 0.5, f"Delete account took too long: {end_time - start_time}s"

    def test_perf_incoming_transfers(self, client):
        pesel = "12345678901"
        payload = {"name": "Perf", "surname": "Transfer", "pesel": pesel}
        
        client.post("/api/accounts", json=payload)
        
        iterations = 100
        transfer_amount = 10
        
        for _ in range(iterations):
            transfer_data = {
                "amount": transfer_amount,
                "type": "incoming"
            }
            
            start_time = time.time()
            response = client.post(f"/api/accounts/{pesel}/transfer", json=transfer_data)
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < 0.5, f"Transfer took too long: {end_time - start_time}s"
            
        response_get = client.get(f"/api/accounts/{pesel}")
        assert response_get.status_code == 200
        
        expected_balance = iterations * transfer_amount
        actual_balance = response_get.json["balance"]
        
        assert actual_balance == expected_balance