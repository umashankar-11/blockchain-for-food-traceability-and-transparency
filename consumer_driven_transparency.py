import hashlib
import json
import time

def calculate_hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def add_block(chain, data):
    if len(chain) == 0:
        previous_hash = "0"
        index = 0
    else:
        previous_hash = chain[-1]['hash']
        index = len(chain)

    block = {
        "index": index,
        "timestamp": time.time(),
        "data": data,
        "previous_hash": previous_hash,
        "hash": calculate_hash({
            "index": index,
            "timestamp": time.time(),
            "data": data,
            "previous_hash": previous_hash
        })
    }

    chain.append(block)

def get_chain(chain):
    return chain

def is_valid(chain):
    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i - 1]

        if current_block['hash'] != calculate_hash({
            "index": current_block['index'],
            "timestamp": current_block['timestamp'],
            "data": current_block['data'],
            "previous_hash": current_block['previous_hash']
        }):
            return False

        if current_block['previous_hash'] != previous_block['hash']:
            return False
    return True

def track_product(chain, product_id):
    product_chain = []
    for block in chain:
        if block['data']['product_id'] == product_id:
            product_chain.append(block)
    return product_chain

def update_product_status(chain, product_id, status):
    for block in chain:
        if block['data']['product_id'] == product_id:
            block['data']['status'] = status
            block['data']['timestamp'] = time.time()

def check_for_fraud(chain, product_id):
    fraudulent_data = []
    for block in chain:
        if block['data']['product_id'] == product_id:
            if block['data']['status'] != "Verified":
                fraudulent_data.append(block)
    return fraudulent_data

def add_product_data(chain, product_id, supplier_name, certification, location, status):
    product_entry = {
        "product_id": product_id,
        "supplier_name": supplier_name,
        "certification": certification,
        "location": location,
        "status": status,
        "timestamp": time.time()
    }
    add_block(chain, product_entry)


product_chain = []

add_product_data(product_chain, "P001", "Supplier A", "Organic Certified", "Farm A", "Verified")
add_product_data(product_chain, "P002", "Supplier B", "Fair Trade Certified", "Farm B", "Verified")

tracked_product = track_product(product_chain, "P001")


update_product_status(product_chain, "P001", "Shipped")


fraudulent_data = check_for_fraud(product_chain, "P001")

is_chain_valid = is_valid(product_chain)

print(json.dumps(get_chain(product_chain), indent=4))

print(json.dumps(fraudulent_data, indent=4))

if is_chain_valid:
    print("Blockchain is valid!")
else:
    print("Blockchain has been tampered with!")
