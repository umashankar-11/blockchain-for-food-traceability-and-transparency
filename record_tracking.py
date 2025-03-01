import hashlib, time, json, datetime

record_file = "records.json"

def load_records():
    try: return json.load(open(record_file, 'r'))
    except: return []

def save_records(records): json.dump(records, open(record_file, 'w'), indent=4)

def add_record(records, data):
    timestamp = str(datetime.datetime.now())
    record = {"data": data, "timestamp": timestamp}
    records.append(record)
    save_records(records)
    return record

def get_records():
    return load_records()

def get_record_by_timestamp(records, timestamp):
    for record in records:
        if record["timestamp"] == timestamp:
            return record
    return None

def get_record_by_hash(records, data_hash):
    for record in records:
        if hashlib.sha256(json.dumps(record["data"], sort_keys=True).encode()).hexdigest() == data_hash:
            return record
    return None

def hash_data(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def update_record(records, timestamp, new_data):
    for record in records:
        if record["timestamp"] == timestamp:
            record["data"] = new_data
            save_records(records)
            return True
    return False

def delete_record(records, timestamp):
    new_records = [record for record in records if record["timestamp"] != timestamp]
    if len(new_records) != len(records):
        save_records(new_records)
        return True
    return False

def example_usage():
    records = load_records()
    data1 = {"product": "apple", "quantity": 10}
    record1 = add_record(records, data1)
    print(f"Added record: {record1}")

    data2 = {"product": "banana", "quantity": 5}
    record2 = add_record(records, data2)
    print(f"Added record: {record2}")

    all_records = get_records()
    print(f"All records: {all_records}")

    record_by_time = get_record_by_timestamp(records, record1["timestamp"])
    print(f"Record by timestamp: {record_by_time}")

    hash_data1 = hash_data(data1)
    record_by_hash_value = get_record_by_hash(records, hash_data1)
    print(f"Record by hash: {record_by_hash_value}")
    update_record(records, record1["timestamp"], {"product": "apple", "quantity": 12})
    delete_record(records, record2["timestamp"])

example_usage()