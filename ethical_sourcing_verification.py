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
        self.next = None

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_block(self, data):
        new_block = Block(len(self), time.time(), data, self.tail.hash if self.tail else "0")
        if self.tail:
            self.tail.next = new_block
        self.tail = new_block
        if not self.head:
            self.head = new_block

    def get_chain(self):
        chain = []
        current = self.head
        while current:
            chain.append(current.__dict__)
            current = current.next
        return chain

    def is_valid(self):
        current = self.head
        while current and current.next:
            if current.hash != current.calculate_hash():
                return False
            if current.next.previous_hash != current.hash:
                return False
            current = current.next
        return True

class EthicalSourcingVerification:
    def __init__(self):
        self.blockchain = Blockchain()

    def add_sourcing_data(self, product_id, supplier_name, certification, country_of_origin, labor_rights_status, environmental_impact):
        sourcing_entry = {
            "product_id": product_id,
            "supplier_name": supplier_name,
            "certification": certification,
            "country_of_origin": country_of_origin,
            "labor_rights_status": labor_rights_status,
            "environmental_impact": environmental_impact,
            "timestamp": time.time()
        }
        self.blockchain.add_block(sourcing_entry)

    def track_sourcing_data(self, product_id):
        sourcing_chain = []
        current = self.blockchain.head
        while current:
            if current.data['product_id'] == product_id:
                sourcing_chain.append(current.__dict__)
            current = current.next
        return sourcing_chain

    def update_sourcing_status(self, product_id, labor_rights_status, environmental_impact):
        current = self.blockchain.head
        while current:
            if current.data['product_id'] == product_id:
                current.data['labor_rights_status'] = labor_rights_status
                current.data['environmental_impact'] = environmental_impact
                current.data['timestamp'] = time.time()
            current = current.next

    def verify_sourcing_chain(self):
        return self.blockchain.is_valid()

    def check_for_ethical_compliance(self, product_id):
        non_compliant_data = []
        current = self.blockchain.head
        while current:
            if current.data['product_id'] == product_id:
                if current.data['labor_rights_status'] != "Compliant" or current.data['environmental_impact'] != "Sustainable":
                    non_compliant_data.append(current.__dict__)
            current = current.next
        return non_compliant_data

ethical_sourcing_system = EthicalSourcingVerification()

ethical_sourcing_system.add_sourcing_data("P001", "Supplier A", "Fair Trade Certified", "Country X", "Compliant", "Sustainable")
ethical_sourcing_system.add_sourcing_data("P001", "Supplier B", "Organic Certified", "Country Y", "Compliant", "Sustainable")
ethical_sourcing_system.add_sourcing_data("P002", "Supplier C", "Fair Trade Certified", "Country Z", "Non-Compliant", "Sustainable")

tracked_sourcing_data = ethical_sourcing_system.track_sourcing_data("P001")

ethical_sourcing_system.update_sourcing_status("P001", "Non-Compliant", "Unsustainable")

non_compliant_data = ethical_sourcing_system.check_for_ethical_compliance("P001")

print(json.dumps(ethical_sourcing_system.blockchain.get_chain(), indent=4))

print(json.dumps(non_compliant_data, indent=4))

if ethical_sourcing_system.verify_sourcing_chain():
    print("Ethical sourcing data is valid!")
else:
    print("Ethical sourcing data has been tampered with!")
