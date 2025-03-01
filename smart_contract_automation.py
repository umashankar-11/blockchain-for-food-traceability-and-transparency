import hashlib, time, json, random, datetime

chain_file = "chain.json"
tx_file = "tx.json"

def load_chain():
    try: return json.load(open(chain_file, 'r'))
    except: return [{'index': 1, 'timestamp': str(datetime.datetime.now()), 'proof': 1, 'prev': '0', 'tx': []}]

def save_chain(chain): json.dump(chain, open(chain_file, 'w'), indent=4)

def load_tx():
    try: return json.load(open(tx_file, 'r'))
    except: return []

def save_tx(tx): json.dump(tx, open(tx_file, 'w'), indent=4)

def create_block(chain, proof, prev):
    block = {'index': len(chain) + 1, 'timestamp': str(datetime.datetime.now()), 'proof': proof, 'prev': prev, 'tx': load_tx()}
    chain.append(block); save_chain(chain); save_tx([])
    return block

def get_prev_block(chain): return chain[-1]

def pow(prev_proof):
    proof = 1; valid = False
    while not valid:
        h = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
        if h[:4] == '0000': valid = True
        else: proof += 1
    return proof

def hash_block(block): return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

def valid_chain(chain):
    prev = chain[0]; i = 1
    while i < len(chain):
        block = chain[i]
        if block['prev'] != hash_block(prev): return False
        prev_proof = prev['proof']; proof = block['proof']
        h = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
        if h[:4] != '0000': return False
        prev = block; i += 1
    return True

def add_tx(tx, sender, receiver, amt):
    tx.append({'sender': sender, 'receiver': receiver, 'amount': amt}); save_tx(tx)
    return len(load_chain())

chain = load_chain(); tx = load_tx()

def sensor_data(): return {'temp': round(random.uniform(2, 8), 2), 'humid': random.randint(50, 80)}

def process(data):
    if data['temp'] > 7:
        add_tx(tx, 'sensor', 'alert', 1)
        prev_block = get_prev_block(chain)
        proof = pow(prev_block['proof'])
        prev_hash = hash_block(prev_block)
        create_block(chain, proof, prev_hash)

while True:
    d = sensor_data(); process(d); time.sleep(3)