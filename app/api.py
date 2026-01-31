from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    if not data or "name" not in data or "surname" not in data or "pesel" not in data:
         return jsonify({"message": "Bad request"}), 400

    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    
    if registry.add_account(account): #sprawdzamy czy duplikat
        return jsonify({"message": "Account created"}), 201
    else:
        return jsonify({"message": "Account with this pesel already exists"}), 409

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.get_all_accounts()
    accounts_data = [
        {
            "name": acc.first_name, 
            "surname": acc.last_name, 
            "pesel": acc.pesel, 
            "balance": acc.balance
        } 
        for acc in accounts
    ]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    count = registry.get_count()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.get_account_by_pesel(pesel)
    if account:
        return jsonify({
            "name": account.first_name, 
            "surname": account.last_name, 
            "pesel": account.pesel,
            "balance": account.balance
        }), 200
    else:
        return jsonify({"message": "Account not found"}), 404

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    account = registry.get_account_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404
    
    data = request.get_json()
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
        
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    if registry.delete_account(pesel):
        return jsonify({"message": "Account deleted"}), 200
    else:
        return jsonify({"message": "Account not found"}), 404
    

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def make_transfer(pesel):
    account = registry.get_account_by_pesel(pesel) #czy konto istnieje
    if not account:
        return jsonify({"message": "Account not found"}), 404

    data = request.get_json()
    if "amount" not in data or "type" not in data:
        return jsonify({"message": "Bad request"}), 400

    amount = data["amount"]
    transfer_type = data["type"]

    if transfer_type == "incoming":
        account.incoming_transfer(amount)
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200

    elif transfer_type == "outgoing":
        if account.outgoing_transfer(amount):
             return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
        else:
             return jsonify({"message": "Insufficient funds"}), 422 # [cite: 380]

    elif transfer_type == "express":
        if account.express_transfer(amount):
             return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
        else:
             return jsonify({"message": "Insufficient funds"}), 422

    else:
        return jsonify({"message": "Unknown transfer type"}), 400


if __name__ == '__main__':
    app.run(debug=True)