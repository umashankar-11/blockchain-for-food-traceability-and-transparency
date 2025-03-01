import hashlib
import json
import time
from typing import List

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

class ProductQualityAssurance:
    def __init__(self):
        self.blockchain = Blockchain()

    def add_quality_check(self, product_id, temperature, humidity, location, status):
        quality_data = {
            "product_id": product_id,
            "temperature": temperature,
            "humidity": humidity,
            "location": location,
            "status": status,
            "timestamp": time.time()
        }
        self.blockchain.add_block(quality_data)

    def track_quality_data(self):
        return self.blockchain.get_chain()

    def verify_quality_assurance(self):
        return self.blockchain.is_valid()

quality_assurance = ProductQualityAssurance()

quality_assurance.add_quality_check("P001", 4.0, 85, "Warehouse A", "Passed")
quality_assurance.add_quality_check("P001", 3.5, 80, "Warehouse B", "Passed")
quality_assurance.add_quality_check("P001", 3.0, 75, "Retail Store A", "Passed")

quality_chain = quality_assurance.track_quality_data()

print(json.dumps(quality_chain, indent=4))

if quality_assurance.verify_quality_assurance():
    print("Quality Assurance data is valid!")
else:
    print("Quality Assurance data is compromised!")
