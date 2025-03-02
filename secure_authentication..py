import hashlib
import json
import time
import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), time.time(), data, previous_block.hash)
        self.chain.append(new_block)

    def get_chain(self):
        return [block.__dict__ for block in self.chain]

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
        return True

class SecureAuth:
    def __init__(self):
        self.private_key, self.public_key = self.generate_keys()
        self.blockchain = Blockchain()

    def generate_keys(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem

    def sign_data(self, data):
        private_key = serialization.load_pem_private_key(self.private_key, password=None, backend=default_backend())
        signature = private_key.sign(
            data.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode()

    def verify_signature(self, data, signature):
        public_key = serialization.load_pem_public_key(self.public_key, backend=default_backend())
        try:
            public_key.verify(
                base64.b64decode(signature),
                data.encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def add_authenticated_entry(self, data):
        signature = self.sign_data(data)
        entry = {
            "data": data,
            "signature": signature,
            "timestamp": time.time()
        }
        self.blockchain.add_block(entry)

    def authenticate_entry(self, data, signature):
        return self.verify_signature(data, signature)

    def get_blockchain(self):
        return self.blockchain.get_chain()

    def verify_chain(self):
        return self.blockchain.is_valid()

auth_system = SecureAuth()

data1 = "Tomatoes harvested from Farm A"
auth_system.add_authenticated_entry(data1)

data2 = "Tomatoes shipped to Warehouse B"
auth_system.add_authenticated_entry(data2)

chain = auth_system.get_blockchain()

print(json.dumps(chain, indent=4))


if auth_system.verify_chain():
    print("Blockchain is valid and secure!")
else:
    print("Blockchain has been tampered with!")


sample_data = "Tomatoes harvested from Farm A"
sample_signature = chain[1]['signature']  
is_authenticated = auth_system.authenticate_entry(sample_data, sample_signature)

if is_authenticated:
    print("Data authentication successful!")
else:
    print("Data authentication failed!")
