from behave import *
import requests

URL = "http://127.0.0.1:5000"

@step('I make an incoming transfer of "{amount}" to account with pesel "{pesel}"')
def make_incoming_transfer(context, amount, pesel):
    json_body = {
        "amount": int(amount),
        "type": "incoming"
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    context.last_response = response # Zapisujemy odpowiedź w kontekście
    assert response.status_code == 200

@when('I make an outgoing transfer of "{amount}" from account with pesel "{pesel}"')
def make_outgoing_transfer(context, amount, pesel):
    json_body = {
        "amount": int(amount),
        "type": "outgoing"
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    context.last_response = response # Zapisujemy odpowiedź, żeby sprawdzić ją w następnym kroku

@then('The transfer should fail with status code "{status_code}"')
def check_transfer_failed(context, status_code):
    assert context.last_response.status_code == int(status_code)