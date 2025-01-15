from flask import Flask, request, jsonify
from web3 import Web3

app = Flask(__name__)

# Connect to Ethereum via Infura
infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
w3 = Web3(Web3.HTTPProvider(infura_url))

@app.route('/balance', methods=['GET'])
def get_balance():
    address = request.args.get('address')
    balance = w3.eth.get_balance(address)
    return jsonify({"address": address, "balance": w3.fromWei(balance, 'ether')})

if __name__ == "__main__":
    app.run(debug=True)

