import os
import json
from web3 import Web3
from eth_account import Account
from bitcoin import *
from cryptography.fernet import Fernet

class DExAwallet:
    def __init__(self):
        # Ethereum & Binance Smart Chain nodes
        self.eth_web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"))  # Ethereum
        self.bsc_web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))  # Binance Smart Chain

        # File to store wallets
        self.wallet_file = "dexawallet.json"
        self.fernet_key = Fernet.generate_key()
        self.cipher = Fernet(self.fernet_key)

    def create_wallet(self, crypto_type):
        """Creates a new wallet for the specified cryptocurrency."""
        if crypto_type == "ETH" or crypto_type == "BSC":
            account = Account.create()
            private_key = account.key.hex()
            address = account.address
        elif crypto_type == "BTC":
            private_key = random_key()
            address = privtopub(private_key)
            address = pubtoaddr(address)
        else:
            print("Unsupported cryptocurrency.")
            return

        encrypted_key = self.cipher.encrypt(private_key.encode()).decode()
        wallet_data = {"crypto": crypto_type, "address": address, "private_key": encrypted_key}

        # Save wallet to file
        self.save_wallet(wallet_data)
        print(f"New {crypto_type} wallet created!\nAddress: {address}\nKeep your private key safe.")

    def save_wallet(self, wallet_data):
        """Saves wallet data to the wallet file."""
        if os.path.exists(self.wallet_file):
            with open(self.wallet_file, "r") as file:
                data = json.load(file)
        else:
            data = []

        data.append(wallet_data)
        with open(self.wallet_file, "w") as file:
            json.dump(data, file, indent=4)

    def load_wallets(self):
        """Loads all wallets from the wallet file."""
        if not os.path.exists(self.wallet_file):
            print("No wallets found. Please create one first.")
            return []
        with open(self.wallet_file, "r") as file:
            wallets = json.load(file)
        return wallets

    def check_balance(self, crypto_type, address):
        """Checks the balance of a specific wallet."""
        if crypto_type == "ETH":
            balance = self.eth_web3.eth.get_balance(address)
            print(f"Balance for {address} (ETH): {self.eth_web3.fromWei(balance, 'ether')} ETH")
        elif crypto_type == "BSC":
            balance = self.bsc_web3.eth.get_balance(address)
            print(f"Balance for {address} (BSC): {self.bsc_web3.fromWei(balance, 'ether')} BNB")
        elif crypto_type == "BTC":
            try:
                url = f"https://blockchain.info/q/addressbalance/{address}"
                balance = requests.get(url).text
                print(f"Balance for {address} (BTC): {int(balance) / 1e8} BTC")
            except Exception as e:
                print(f"Error checking BTC balance: {e}")
        else:
            print("Unsupported cryptocurrency.")

    def send_transaction(self, crypto_type, from_wallet, to_address, amount):
        """Sends a transaction from a wallet."""
        private_key = from_wallet["private_key"]
        private_key = self.cipher.decrypt(private_key.encode()).decode()

        if crypto_type == "ETH" or crypto_type == "BSC":
            web3 = self.eth_web3 if crypto_type == "ETH" else self.bsc_web3
            nonce = web3.eth.get_transaction_count(from_wallet["address"])
            tx = {
                "nonce": nonce,
                "to": to_address,
                "value": web3.toWei(amount, "ether"),
                "gas": 21000,
                "gasPrice": web3.toWei("50", "gwei"),
            }
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"{crypto_type} Transaction sent! Hash: {web3.toHex(tx_hash)}")
        elif crypto_type == "BTC":
            try:
                tx = mktx(privtoaddr(private_key), [(to_address, amount * 1e8)])
                signed_tx = sign(tx, 0, private_key)
                print(f"BTC Transaction signed: {signed_tx}")
            except Exception as e:
                print(f"Error sending BTC transaction: {e}")
        else:
            print("Unsupported cryptocurrency.")

    def menu(self):
        """Displays the wallet menu."""
        while True:
            print("\nDExAwallet Menu:")
            print("1. Create Wallet")
            print("2. Load Wallets")
            print("3. Check Balance")
            print("4. Send Transaction")
            print("5. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                crypto = input("Enter cryptocurrency (ETH, BTC, BSC): ").upper()
                self.create_wallet(crypto)
            elif choice == "2":
                wallets = self.load_wallets()
                if wallets:
                    for w in wallets:
                        print(f"{w['crypto']} Wallet: {w['address']}")
            elif choice == "3":
                crypto = input("Enter cryptocurrency (ETH, BTC, BSC): ").upper()
                address = input("Enter wallet address: ")
                self.check_balance(crypto, address)
            elif choice == "4":
                crypto = input("Enter cryptocurrency (ETH, BTC, BSC): ").upper()
                from_address = input("Enter your wallet address: ")
                to_address = input("Enter recipient address: ")
                amount = float(input("Enter amount: "))
                wallets = self.load_wallets()
                wallet = next((w for w in wallets if w["address"] == from_address and w["crypto"] == crypto), None)
                if wallet:
                    self.send_transaction(crypto, wallet, to_address, amount)
                else:
                    print("Wallet not found.")
            elif choice == "5":
                print("Exiting DExAwallet. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    wallet = DExAwallet()
    wallet.menu()
