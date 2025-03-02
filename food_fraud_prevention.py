import hashlib
import json
import time

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

class FoodFraudPrevention:
    def __init__(self):
        self.blockchain = Blockchain()
        self.food_data = {}

    def add_food_data(self, product_id, source, certification, batch, location, status):
        food_entry = {
            "product_id": product_id,
            "source": source,
            "certification": certification,
            "batch": batch,
            "location": location,
            "status": status,
            "timestamp": time.time()
        }
        self.blockchain.add_block(food_entry)

    def track_food_item(self, product_id):
        food_chain = []
        for block in self.blockchain.get_chain():
            if block['data']['product_id'] == product_id:
                food_chain.append(block)
        return food_chain

    def update_food_status(self, product_id, status):
        for block in self.blockchain.get_chain():
            if block['data']['product_id'] == product_id:
                block['data']['status'] = status
                block['data']['timestamp'] = time.time()

    def verify_food_chain(self):
        return self.blockchain.is_valid()

    def check_for_fraud(self, product_id):
        fraudulent_data = []
        for block in self.blockchain.get_chain():
            if block['data']['product_id'] == product_id:
                if block['data']['status'] != "Verified":
                    fraudulent_data.append(block)
        return fraudulent_data


fraud_prevention_system = FoodFraudPrevention()

fraud_prevention_system.add_food_data("P001", "Farm A", "Organic", "B001", "Warehouse A", "Verified")
fraud_prevention_system.add_food_data("P001", "Warehouse A", "Organic", "B001", "Retail Store A", "Verified")
fraud_prevention_system.add_food_data("P002", "Farm B", "Non-GMO", "B002", "Warehouse B", "Verified")

tracked_food = fraud_prevention_system.track_food_item("P001")

fraud_prevention_system.update_food_status("P001", "Spoiled")

fraudulent_food = fraud_prevention_system.check_for_fraud("P001")

print(json.dumps(fraud_prevention_system.blockchain.get_chain(), indent=4))

print(json.dumps(fraudulent_food, indent=4))

if fraud_prevention_system.verify_food_chain():
    print("Food chain is valid!")
else:
    print("Food chain has been tampered with!")
