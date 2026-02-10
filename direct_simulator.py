import time
import json
import pandas as pd
import requests
import random
import joblib

# Load model
model = joblib.load("fog_node/model.pkl")

# Load data
df = pd.read_csv("patient_simulator/mitbih_hr.csv")

CLOUD_ALERT_API = "http://127.0.0.1:5000/api/alerts"
CLOUD_HEALTH_API = "http://127.0.0.1:5000/api/health"

print("Direct simulator started (no MQTT needed)")

for _, row in df.iterrows():
    base_hr = int(row["hr"])
    r = random.random()

    # 70% NORMAL
    if r < 0.7:
        hr = base_hr
        acc = round(random.uniform(0.8, 1.2), 2)
    # 30% CRITICAL
    else:
        hr = random.randint(150, 180)
        acc = round(random.uniform(20, 25), 2)

    spo2 = float(row["spo2"])
    temp = float(row["temp"])

    # ML prediction
    pred = model.predict([[hr, spo2, temp, acc]])[0]

    # Determine status
    if acc > 20 or hr > 140:
        status = "CRITICAL"
    elif pred == -1:
        status = "WARNING"
    else:
        status = "NORMAL"

    # Prepare data
    health = {
        "patient_id": "P001",
        "status": status,
        "hr": hr,
        "spo2": spo2,
        "temp": temp,
        "acc_mag": acc,
        "timestamp": time.time()
    }

    # Send to cloud
    try:
        requests.post(CLOUD_HEALTH_API, json=health)
        
        if status == "CRITICAL":
            alert = health.copy()
            alert["type"] = "CRITICAL"
            requests.post(CLOUD_ALERT_API, json=alert)
            print(f"🚨 CRITICAL: HR={hr}, ACC={acc}")
        else:
            print(f"✓ {status}: HR={hr}, ACC={acc}")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(2)
