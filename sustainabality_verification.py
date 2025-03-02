import hashlib
import json
import time
import os

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

class SustainabilityVerification:
    def __init__(self):
        self.blockchain = Blockchain()

    def add_sustainability_data(self, product_id, sustainability_type, certification, verification_date, location):
        sustainability_entry = {
            "product_id": product_id,
            "sustainability_type": sustainability_type,
            "certification": certification,
            "verification_date": verification_date,
            "location": location,
            "timestamp": time.time()
        }
        self.blockchain.add_block(sustainability_entry)

    def track_sustainability(self):
        return self.blockchain.get_chain()

    def verify_sustainability_chain(self):
        return self.blockchain.is_valid()

sustainability_system = SustainabilityVerification()

sustainability_system.add_sustainability_data("P001", "Organic", "USDA Organic", "2025-03-01", "Farm A")
sustainability_system.add_sustainability_data("P001", "Fair Trade", "Fair Trade Certified", "2025-03-02", "Farm A")
sustainability_system.add_sustainability_data("P002", "Eco-friendly", "Green Seal Certified", "2025-03-01", "Farm B")

sustainability_chain = sustainability_system.track_sustainability()

print(json.dumps(sustainability_chain, indent=4))

if sustainability_system.verify_sustainability_chain():
    print("Sustainability chain is valid!")
else:
    print("Sustainability data is compromised!")
