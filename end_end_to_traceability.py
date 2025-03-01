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

class FoodTraceability:
    def __init__(self):
        self.blockchain = Blockchain()

    def add_item_entry(self, origin, product_details, location):
        entry_data = {
            "origin": origin,
            "product_details": product_details,
            "location": location,
            "timestamp": time.time()
        }
        self.blockchain.add_block(entry_data)

    def track_item(self):
        return self.blockchain.get_chain()

    def verify_traceability(self):
        return self.blockchain.is_valid()


food_trace = FoodTraceability()

food_trace.add_item_entry("Farm A", {"product": "Tomatoes", "quantity": 1000}, "Farm Location A")

food_trace.add_item_entry("Warehouse B", {"product": "Tomatoes", "quantity": 1000}, "Warehouse Location B")

food_trace.add_item_entry("Retail Store C", {"product": "Tomatoes", "quantity": 1000}, "Retail Store Location C")

trace_chain = food_trace.track_item()

print(json.dumps(trace_chain, indent=4))


if food_trace.verify_traceability():
    print("Traceability is valid!")
else:
    print("Traceability is compromised!")
