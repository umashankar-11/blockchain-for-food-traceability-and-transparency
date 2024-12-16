import hashlib
import json
import time
import os
import random


class Block:
    def __init__(self, index, food_item, robot_action, timestamp, previous_hash):
        self.index = index
        self.food_item = food_item
        self.robot_action = robot_action
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + str(self.food_item) + str(self.robot_action) + str(self.timestamp) + str(self.previous_hash)
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_food_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # The first block has index 0 and arbitrary previous hash
        genesis_block = Block(0, "Genesis Block", "No Robot Action", time.time(), "0")
        self.chain.append(genesis_block)

    def add_food_transaction(self, food_item, robot_action):
        self.current_food_transactions.append((food_item, robot_action))

    def create_new_block(self):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), self.current_food_transactions, "Robot Action", time.time(), last_block.hash)
        self.chain.append(new_block)
        self.current_food_transactions = []
        self.store_block_data(new_block)

    def store_block_data(self, block):
        """Save block data to a file for traceability."""
        filename = "block_data.txt"
        with open(filename, 'a') as file:
            file.write(f"Block Index: {block.index}\n")
            file.write(f"Food Item: {json.dumps(block.food_item)}\n")
            file.write(f"Robot Action: {block.robot_action}\n")
            file.write(f"Timestamp: {block.timestamp}\n")
            file.write(f"Previous Hash: {block.previous_hash}\n")
            file.write(f"Hash: {block.hash}\n\n")

    def get_last_block(self):
        return self.chain[-1]

    def trace_food_item(self, food_item_id):
        """Trace a food item in the blockchain."""
        for block in self.chain:
            for food_item in block.food_item:
             if food_item[id] == food_item_id:
                print(f"Found in Block {block.index}: {food_item}, Robot Action: {food_item['robot_action']}")
            return food_item
    print("Food item not found in the blockchain.")

# ---------------------------


class Robot:
    def __init__(self, robot_id, task, location="Unknown"):
        self.robot_id = robot_id
        self.task = task  
        self.location = location  

    def perform_task(self, food_item, action_details):
        """Simulate the robot performing a task and checking food quality."""
        self.location = action_details.get('location', "Unknown")
        robot_action = f"Robot {self.robot_id} performed {self.task} at {self.location}."
        food_item['robot_action'] = robot_action
        print(f"Robot Action: {robot_action}")
        return robot_action

# ---------------------------


class QualityCheck:
    def __init__(self):
        # Simulate a basic ML model for food quality check
        self.model = {"Apple": "Good", "Banana": "Average", "Orange": "Poor"}

    def check_quality(self, food_type):
        """Check food quality using a predefined ML model."""
        quality = self.model.get(food_type, "Unknown")
        return quality



class FoodTraceability:
    def __init__(self):
        self.blockchain = Blockchain()
        self.food_registry = {}
        self.robot_registry = {}
        self.quality_check = QualityCheck()
        self.alerts = []

    def register_food_item(self, food_item_id, food_origin, food_type, certifications, best_before_date, nutritional_info):
        food_item = {
            "id": food_item_id,
            "origin": food_origin,
            "type": food_type,
            "certifications": certifications,
            "status": "Registered",
            "best_before_date": best_before_date,
            "nutritional_info": nutritional_info,
            "quality": self.quality_check.check_quality(food_type),
            "robot_action": None
        }
        self.food_registry[food_item_id] = food_item
        print(f"Food item {food_item_id} registered.")
        self.blockchain.add_food_transaction(food_item, "No Robot Action")

    def process_food_item(self, food_item_id, processing_location, processing_type):
        if food_item_id not in self.food_registry:
            print("Food item not found!")
            return
        food_item = self.food_registry[food_item_id]
        food_item['status'] = "Processed"
        food_item['processing_location'] = processing_location
        food_item['processing_type'] = processing_type
        food_item['quality'] = self.quality_check.check_quality(food_item['type'])
        print(f"Food item {food_item_id} processed with quality: {food_item['quality']}.")
        self.blockchain.add_food_transaction(food_item, "No Robot Action")

    def ship_food_item(self, food_item_id, destination):
        if food_item_id not in self.food_registry:
            print("Food item not found!")
            return
        food_item = self.food_registry[food_item_id]
        food_item['status'] = "Shipped"
        food_item['destination'] = destination
        print(f"Food item {food_item_id} shipped to {destination}.")
        self.blockchain.add_food_transaction(food_item, "No Robot Action")

    def receive_food_item(self, food_item_id, store_location):
        if food_item_id not in self.food_registry:
            print("Food item not found!")
            return
        food_item = self.food_registry[food_item_id]
        food_item['status'] = "Received"
        food_item['store_location'] = store_location
        print(f"Food item {food_item_id} received at {store_location}.")
        self.blockchain.add_food_transaction(food_item, "No Robot Action")

    def log_robot_action(self, robot, food_item_id, action_details):
        """Log the robot's action into the blockchain"""
        if food_item_id not in self.food_registry:
            print("Food item not found!")
            return
        food_item = self.food_registry[food_item_id]
        robot_action = robot.perform_task(food_item, action_details)
        self.blockchain.add_food_transaction(food_item, robot_action)

    def generate_report(self):
        """Generate a report of all food items and their traceability."""
        print("\nGenerating Food Traceability Report...")
        for food_item_id, food_item in self.food_registry.items():
            print(f"Food Item ID: {food_item_id}")
            print(f"Origin: {food_item['origin']}")
            print(f"Type: {food_item['type']}")
            print(f"Status: {food_item['status']}")
            print(f"Best Before Date: {food_item['best_before_date']}")
            print(f"Nutritional Info: {json.dumps(food_item['nutritional_info'])}")
            print(f"Quality: {food_item['quality']}")
            print(f"Last Robot Action: {food_item['robot_action']}\n")

    def send_alert(self, message):
        """Send an alert."""
        self.alerts.append(message)
        print(f"ALERT: {message}")

    def display_food_item_info(self, food_item_id):
        """Display all information related to a food item."""
        if food_item_id not in self.food_registry:
            print("Food item not found!")
            return
        food_item = self.food_registry[food_item_id]
        print(f"Food Item {food_item_id}: {json.dumps(food_item, indent=4)}")

    def validate_integrity(self):
        """Check the integrity of the blockchain."""
        for i in range(1, len(self.blockchain.chain)):
            current_block = self.blockchain.chain[i]
            previous_block = self.blockchain.chain[i - 1]

            
            if current_block.previous_hash != previous_block.hash:
                self.send_alert("Blockchain integrity compromised!")
                return False

        print("Blockchain integrity verified.")
        return True


def main():
    food_system = FoodTraceability()

   
    food_system.register_food_item("001", "Farm A", "Apple", ["Organic"], "2025-12-31", {"Calories": 95, "Carbs": 25, "Fiber": 4.5})
    food_system.register_food_item("002", "Farm B", "Banana", ["Fair Trade", "Organic"], "2025-07-15", {"Calories": 105, "Carbs": 27, "Fiber": 3.1})

    
    food_system.process_food_item("001", "Processing Plant A", "Washed and Packaged")
    food_system.process_food_item("002", "Processing Plant B", "Ripe Stage Checked")

    
    robot1 = Robot(1, "Quality Check")
    robot2 = Robot(2, "Packaging")
    
    
    food_system.log_robot_action(robot1, "001", {'location': "Processing Plant A"})
    food_system.log_robot_action(robot2, "002", {'location': "Processing Plant B"})
    
    
    food_system.ship_food_item("001", "Warehouse A")
    food_system.ship_food_item("002", "Warehouse B")

    
    food_system.receive_food_item("001", "Store A")
    food_system.receive_food_item("002", "Store B")

    
    food_system.blockchain.trace_food_item("001")
    food_system.blockchain.trace_food_item("002")

   
    food_system.generate_report()

    
    food_system.validate_integrity()

    
    food_system.blockchain.create_new_block()

    
    food_system.blockchain.trace_food_item("001")
    food_system.blockchain.trace_food_item("002")

if __name__ == "__main__":
    main()
