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

class SupplyChainOptimization:
    def __init__(self):
        self.blockchain = Blockchain()
        self.inventory = {}

    def add_product(self, product_id, quantity, location, stage):
        product_data = {
            "product_id": product_id,
            "quantity": quantity,
            "location": location,
            "stage": stage,
            "timestamp": time.time()
        }
        self.blockchain.add_block(product_data)
        if product_id in self.inventory:
            self.inventory[product_id] += quantity
        else:
            self.inventory[product_id] = quantity

    def update_inventory(self, product_id, quantity, action):
        if action == 'add':
            if product_id in self.inventory:
                self.inventory[product_id] += quantity
            else:
                self.inventory[product_id] = quantity
        elif action == 'remove':
            if product_id in self.inventory and self.inventory[product_id] >= quantity:
                self.inventory[product_id] -= quantity

    def track_product(self, product_id):
        product_chain = []
        for block in self.blockchain.get_chain():
            if block['data']['product_id'] == product_id:
                product_chain.append(block)
        return product_chain

    def optimize_supply_chain(self):
        optimized_data = []
        for product_id, quantity in self.inventory.items():
            if quantity > 100:  
                optimized_data.append({
                    "product_id": product_id,
                    "quantity": quantity,
                    "optimization_status": "Replenish"
                })
            elif quantity < 10:  
                optimized_data.append({
                    "product_id": product_id,
                    "quantity": quantity,
                    "optimization_status": "Restock"
                })
            else:
                optimized_data.append({
                    "product_id": product_id,
                    "quantity": quantity,
                    "optimization_status": "Balanced"
                })
        return optimized_data

    def verify_supply_chain(self):
        return self.blockchain.is_valid()

supply_chain = SupplyChainOptimization()

supply_chain.add_product("P001", 50, "Warehouse A", "Received")
supply_chain.add_product("P001", 70, "Warehouse A", "Stored")
supply_chain.add_product("P002", 10, "Warehouse B", "Shipped")
supply_chain.add_product("P003", 200, "Warehouse C", "Received")

supply_chain.update_inventory("P001", 20, 'add')
supply_chain.update_inventory("P002", 5, 'remove')

tracked_product = supply_chain.track_product("P001")

optimized_supply = supply_chain.optimize_supply_chain()

print(json.dumps(supply_chain.blockchain.get_chain(), indent=4))

print(json.dumps(optimized_supply, indent=4))

if supply_chain.verify_supply_chain():
    print("Supply chain is optimized and valid!")
else:
    print("Supply chain data is compromised!")
