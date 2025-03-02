import json, datetime

waste_file = "waste_data.json"
inventory_file = "inventory.json"

def load_data(file):
    try: return json.load(open(file, 'r'))
    except: return []

def save_data(data, file): json.dump(data, open(file, 'w'), indent=4)

def record_waste(waste_data, item, quantity, reason):
    time = str(datetime.datetime.now())
    waste_data.append({"item": item, "quantity": quantity, "reason": reason, "time": time})
    save_data(waste_data, waste_file)

def update_inventory(inventory, item, quantity, action):
    found = False
    for i in range(len(inventory)):
        if inventory[i]["item"] == item:
            if action == "add": inventory[i]["quantity"] += quantity
            elif action == "remove": inventory[i]["quantity"] -= quantity
            found = True
            break
    if not found and action == "add": inventory.append({"item": item, "quantity": quantity})
    save_data(inventory, inventory_file)

def generate_report(waste_data):
    report = {}
    for entry in waste_data:
        item = entry["item"]
        if item not in report: report[item] = {"quantity": 0, "reasons": {}}
        report[item]["quantity"] += entry["quantity"]
        reason = entry["reason"]
        if reason not in report[item]["reasons"]: report[item]["reasons"][reason] = 0
        report[item]["reasons"][reason] += 1
    return report

def example_tracking():
    waste = load_data(waste_file)
    inventory = load_data(inventory_file)

    update_inventory(inventory, "apples", 100, "add")
    record_waste(waste, "apples", 10, "spoiled")
    update_inventory(inventory, "apples", 10, "remove")

    update_inventory(inventory, "bananas", 50, "add")
    record_waste(waste, "bananas", 5, "bruised")
    update_inventory(inventory, "bananas", 5, "remove")

    report = generate_report(waste)
    print(json.dumps(report, indent=4))

example_tracking()