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

class DecentralizedIdentity:
    def __init__(self):
        self.blockchain = Blockchain()

    def create_identity(self, user_id, public_key, personal_data):
        identity_entry = {
            "user_id": user_id,
            "public_key": public_key,
            "personal_data": personal_data,
            "timestamp": time.time()
        }
        self.blockchain.add_block(identity_entry)

    def update_identity(self, user_id, new_public_key=None, new_personal_data=None):
        current = self.blockchain.head
        while current:
            if current.data['user_id'] == user_id:
                if new_public_key:
                    current.data['public_key'] = new_public_key
                if new_personal_data:
                    current.data['personal_data'] = new_personal_data
                current.data['timestamp'] = time.time()
            current = current.next

    def get_identity(self, user_id):
        identity_chain = []
        current = self.blockchain.head
        while current:
            if current.data['user_id'] == user_id:
                identity_chain.append(current.__dict__)
            current = current.next
        return identity_chain

    def verify_identity(self):
        return self.blockchain.is_valid()


identity_system = DecentralizedIdentity()

identity_system.create_identity("U001", "public_key_001", {"name": "Alice", "age": 30, "address": "123 Street"})
identity_system.create_identity("U002", "public_key_002", {"name": "Bob", "age": 25, "address": "456 Avenue"})

identity_system.update_identity("U001", new_public_key="updated_public_key_001", new_personal_data={"name": "Alice", "age": 31, "address": "123 Street Updated"})

retrieved_identity = identity_system.get_identity("U001")

identity_is_valid = identity_system.verify_identity()

print(json.dumps(identity_system.blockchain.get_chain(), indent=4))

print(json.dumps(retrieved_identity, indent=4))

if identity_is_valid:
    print("Identity data is valid!")
else:
    print("Identity data has been tampered with!")
