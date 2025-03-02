import json, datetime, hashlib

records_file = "records.json"
alerts_file = "alerts.json"

def load_records():
    try: return json.load(open(records_file, 'r'))
    except: return []

def save_records(records): json.dump(records, open(records_file, 'w'), indent=4)

def load_alerts():
    try: return json.load(open(alerts_file, 'r'))
    except: return []

def save_alerts(alerts): json.dump(alerts, open(alerts_file, 'w'), indent=4)

def add_record(records, data, batch_id):
    timestamp = str(datetime.datetime.now())
    record = {"data": data, "timestamp": timestamp, "batch_id": batch_id}
    records.append(record); save_records(records); return record

def check_records(records, alert_condition):
    alerts = []
    for record in records:
        if alert_condition(record["data"]):
            alerts.append({"record": record, "alert_time": str(datetime.datetime.now())})
    return alerts

def generate_recall_list(alerts):
    recall_list = {}
    for alert in alerts:
        batch_id = alert["record"]["batch_id"]
        if batch_id not in recall_list:
            recall_list[batch_id] = []
        recall_list[batch_id].append(alert["record"])
    return recall_list

def trigger_recall(recall_list):
    print("Recall triggered:")
    print(json.dumps(recall_list, indent=4))

def example_usage():
    records = load_records()
    add_record(records, {"product": "milk", "temp": 4, "batch_id": "batch123"}, "batch123")
    add_record(records, {"product": "milk", "temp": 8, "batch_id": "batch123"}, "batch123")
    add_record(records, {"product": "milk", "temp": 3, "batch_id": "batch456"}, "batch456")
    add_record(records, {"product": "milk", "temp": 9, "batch_id": "batch789"}, "batch789")

    alert_condition = lambda data: data.get("temp", 0) > 7
    alerts = check_records(records, alert_condition)
    save_alerts(alerts)

    recall_list = generate_recall_list(alerts)
    trigger_recall(recall_list)

example_usage()