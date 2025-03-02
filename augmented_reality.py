import hashlib
import json
import time
import cv2
import numpy as np

# Blockchain functions
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

def add_product_data(chain, product_id, supplier_name, production_date, expiry_date, status, batch_code, certification):
    product_entry = {
        "product_id": product_id,
        "supplier_name": supplier_name,
        "production_date": production_date,
        "expiry_date": expiry_date,
        "status": status,
        "batch_code": batch_code,
        "certification": certification,
        "timestamp": time.time()
    }
    add_block(chain, product_entry)

def get_product_info(chain, product_id):
    product_info = []
    for block in chain:
        if block['data']['product_id'] == product_id:
            product_info.append(block)
    return product_info


aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters_create()

camera_matrix = np.array([[600, 0, 320], [0, 600, 240], [0, 0, 1]], dtype=np.float32)
dist_coeffs = np.zeros((5, 1))

cap = cv2.VideoCapture(0)

product_chain = []

add_product_data(product_chain, "P001", "Supplier A", "2025-03-01", "2026-03-01", "Verified", "BATCH1234", "ISO Certified")
add_product_data(product_chain, "P002", "Supplier B", "2025-02-01", "2026-02-01", "Unverified", "BATCH1235", "Non-Certified")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.1, camera_matrix, dist_coeffs)

        for i in range(len(ids)):
            cv2.aruco.drawAxis(frame, camera_matrix, dist_coeffs, rvec[i], tvec[i], 0.1)

            cube_points = np.array([
                [-0.05, -0.05, 0],
                [ 0.05, -0.05, 0],
                [ 0.05,  0.05, 0],
                [-0.05,  0.05, 0],
                [-0.05, -0.05, 0.1],
                [ 0.05, -0.05, 0.1],
                [ 0.05,  0.05, 0.1],
                [-0.05,  0.05, 0.1]
            ], dtype=np.float32)

            cube_points = np.dot(cube_points, np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
            cube_points = cube_points + np.array([0, 0, 0.1])

            img_points, _ = cv2.projectPoints(cube_points, rvec[i], tvec[i], camera_matrix, dist_coeffs)

            img_points = img_points.reshape(-1, 2)
            for j in range(4):
                cv2.line(frame, tuple(img_points[j]), tuple(img_points[(j + 1) % 4]), (0, 255, 0), 3)
                cv2.line(frame, tuple(img_points[j + 4]), tuple(img_points[(j + 1) % 4 + 4]), (0, 255, 0), 3)
                cv2.line(frame, tuple(img_points[j]), tuple(img_points[j + 4]), (0, 255, 0), 3)

         
            product_id = str(ids[i][0])  
            product_info = get_product_info(product_chain, product_id)
            if product_info:
                product_details = product_info[0]['data']
                product_text = f"Product ID: {product_details['product_id']}\n" \
                               f"Supplier: {product_details['supplier_name']}\n" \
                               f"Certification: {product_details['certification']}"
                cv2.putText(frame, product_text, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Augmented Reality with Blockchain', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
