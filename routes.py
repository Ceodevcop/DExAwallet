from flask import Flask, request, jsonify
from web3 import Web3

app = Flask(__name__)

INFURA_URL = "https://mainnet.infura.io/v3/<your-infura-project-id>"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

@app.route("/balance", methods=["GET"])
def get_balance():
    address = request.args.get("address")
    if not Web3.isAddress(address):
        return jsonify({"error": "Invalid address"}), 400
    balance = w3.eth.get_balance(address)
    return jsonify({"address": address, "balance": w3.fromWei(balance, 'ether')})

