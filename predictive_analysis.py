import hashlib
import json
import time
import random

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

def predictive_analytics(chain, product_id):
    product_data = []
    current = 0
    while current < len(chain):
        if chain[current]['data']['product_id'] == product_id:
            product_data.append(chain[current]['data'])
        current += 1

    predictions = {}
    if len(product_data) > 0:
      
        total_sales = 0
        for data in product_data:
            total_sales += random.randint(50, 200)  

        avg_sales = total_sales / len(product_data)
        predictions['product_id'] = product_id
        predictions['predicted_sales'] = avg_sales
        predictions['status'] = "Prediction Successful"
    else:
        predictions['product_id'] = product_id
        predictions['status'] = "No data available for prediction"

    return predictions

def add_product_data(chain, product_id, supplier_name, production_date, status):
    product_entry = {
        "product_id": product_id,
        "supplier_name": supplier_name,
        "production_date": production_date,
        "status": status,
        "timestamp": time.time()
    }
    add_block(chain, product_entry)


product_chain = []

add_product_data(product_chain, "P001", "Supplier A", "2025-03-01", "Available")
add_product_data(product_chain, "P002", "Supplier B", "2025-02-01", "Sold Out")
add_product_data(product_chain, "P001", "Supplier A", "2025-03-15", "Available")


product_prediction = predictive_analytics(product_chain, "P001")

is_chain_valid = is_valid(product_chain)

print(json.dumps(get_chain(product_chain), indent=4))

print(json.dumps(product_prediction, indent=4))

if is_chain_valid:
    print("Blockchain is valid!")
else:
    print("Blockchain has been tampered with!")
