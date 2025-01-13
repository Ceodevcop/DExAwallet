from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
import os

def generate_private_key():
    private_key = ec.generate_private_key(ec.SECP256K1())
    return private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())

def save_key_to_file(key, filename="private_key.pem"):
    with open(filename, "wb") as f:
        f.write(key)

