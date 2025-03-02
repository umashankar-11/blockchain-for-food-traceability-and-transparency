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

def track_package(chain, product_id):
    package_chain = []
    current = 0
    while current < len(chain):
        if chain[current]['data']['product_id'] == product_id:
            package_chain.append(chain[current])
        current += 1
    return package_chain

def update_package_status(chain, product_id, status):
    current = 0
    while current < len(chain):
        if chain[current]['data']['product_id'] == product_id:
            chain[current]['data']['status'] = status
            chain[current]['data']['timestamp'] = time.time()
        current += 1

def check_for_fraud(chain, product_id):
    fraudulent_data = []
    current = 0
    while current < len(chain):
        if chain[current]['data']['product_id'] == product_id:
            if chain[current]['data']['status'] != "Verified":
                fraudulent_data.append(chain[current])
        current += 1
    return fraudulent_data

def add_package_data(chain, product_id, packaging_material, production_date, expiration_date, status):
    package_entry = {
        "product_id": product_id,
        "packaging_material": packaging_material,
        "production_date": production_date,
        "expiration_date": expiration_date,
        "status": status,
        "timestamp": time.time()
    }
    add_block(chain, package_entry)

package_chain = []

add_package_data(package_chain, "P001", "Biodegradable", "2025-03-01", "2026-03-01", "Verified")
add_package_data(package_chain, "P002", "Recyclable", "2025-02-01", "2026-02-01", "Verified")


tracked_package = track_package(package_chain, "P001")

update_package_status(package_chain, "P001", "Shipped")

fraudulent_data = check_for_fraud(package_chain, "P001")

is_chain_valid = is_valid(package_chain)

print(json.dumps(get_chain(package_chain), indent=4))

print(json.dumps(fraudulent_data, indent=4))

if is_chain_valid:
    print("Blockchain is valid!")
else:
    print("Blockchain has been tampered with!")
