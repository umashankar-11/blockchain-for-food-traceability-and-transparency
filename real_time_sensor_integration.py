import time, random, hashlib, datetime, json

config = {
    "BLOCKCHAIN_API_URL": "http://your-blockchain-api.com/add_data",
    "SENSOR_READING_INTERVAL": 3,
    "SENSOR_ID": "sensor-123",
    "PRODUCT_ID": "product-456"
}

def get_sensor_data():
    temp = round(random.uniform(2, 8), 2)
    humid = random.randint(50, 80)
    press = round(random.uniform(980, 1020), 2)
    time_stamp = datetime.datetime.now().isoformat()
    return {
        "sensor_id": config["SENSOR_ID"],
        "product_id": config["PRODUCT_ID"],
        "temperature": temp,
        "humidity": humid,
        "pressure": press,
        "timestamp": time_stamp
    }

def add_to_blockchain(data):
    data_str = json.dumps(data).encode('utf-8')
    data_hash = hashlib.sha256(data_str).hexdigest()
    print(f"Adding data: Hash: {data_hash}, Data: {data}")
    return data_hash

def main():
    try:
        while True:
            sensor_data = get_sensor_data()
            returned_hash = add_to_blockchain(sensor_data)
            verify_data(sensor_data, returned_hash)
            time.sleep(config["SENSOR_READING_INTERVAL"])
    except KeyboardInterrupt:
        print("Sensor simulation stopped.")

def verify_data(data, stored_hash):
    data_str = json.dumps(data).encode('utf-8')
    calculated_hash = hashlib.sha256(data_str).hexdigest()
    if calculated_hash == stored_hash:
        print("Verification: Success.")
    else:
        print("Verification: Failed.")

def retrieve_data(hash_to_retrieve):
    print(f"Retrieving data: Hash: {hash_to_retrieve}")
    retrieved_data = {
        "sensor_id": config["SENSOR_ID"],
        "product_id": config["PRODUCT_ID"],
        "temperature": 6.12,
        "humidity": 72,
        "pressure": 1005.5,
        "timestamp": "2023-10-27T12:00:00"
    }
    retrieved_hash = hashlib.sha256(json.dumps(retrieved_data).encode('utf-8')).hexdigest()
    if retrieved_hash == hash_to_retrieve:
        print(f"Retrieved: {retrieved_data}")
        return retrieved_data
    else:
        print("Data not found/mismatch.")
        return None

if __name__ == "__main__":
    main()

example_data = get_sensor_data()
example_hash = hashlib.sha256(json.dumps(example_data).encode('utf-8')).hexdigest()
retrieve_data(example_hash)