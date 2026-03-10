import time
import json
import pandas as pd
import requests
import random
import joblib
import sys

# Load model
try:
    model = joblib.load("fog_node/model.pkl")
    print("✓ ML model loaded successfully")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    sys.exit(1)

# Load data
try:
    df = pd.read_csv("patient_simulator/mitbih_hr.csv")
    print(f"✓ Loaded {len(df)} patient records")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    sys.exit(1)

CLOUD_ALERT_API = "http://127.0.0.1:5000/api/alerts"
CLOUD_HEALTH_API = "http://127.0.0.1:5000/api/health"

print("=" * 60)
print("🏥 SMART HEALTHCARE MONITORING - PATIENT SIMULATOR")
print("=" * 60)
print("Direct simulator started (no MQTT needed)")
print(f"Backend API: {CLOUD_HEALTH_API}")
print(f"Generating data every 2 seconds...")
print("=" * 60)

iteration = 0
normal_count = 0
critical_count = 0
warning_count = 0

try:
    for _, row in df.iterrows():
        iteration += 1
        base_hr = int(row["hr"])
        r = random.random()

        # 70% NORMAL, 30% CRITICAL
        if r < 0.7:
            hr = base_hr
            acc = round(random.uniform(0.8, 1.2), 2)
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
            critical_count += 1
        elif pred == -1:
            status = "WARNING"
            warning_count += 1
        else:
            status = "NORMAL"
            normal_count += 1

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
            response = requests.post(CLOUD_HEALTH_API, json=health, timeout=5)
            
            if status == "CRITICAL":
                alert = health.copy()
                alert["type"] = "CRITICAL"
                requests.post(CLOUD_ALERT_API, json=alert, timeout=5)
                print(f"[{iteration:04d}] 🚨 CRITICAL: HR={hr} bpm, SpO2={spo2}%, Temp={temp}°C, ACC={acc}g")
            elif status == "WARNING":
                print(f"[{iteration:04d}] ⚠️  WARNING: HR={hr} bpm, SpO2={spo2}%, Temp={temp}°C, ACC={acc}g")
            else:
                print(f"[{iteration:04d}] ✓ NORMAL: HR={hr} bpm, SpO2={spo2}%, Temp={temp}°C, ACC={acc}g")
                
        except requests.exceptions.RequestException as e:
            print(f"[{iteration:04d}] ✗ Connection Error: {e}")
        except Exception as e:
            print(f"[{iteration:04d}] ✗ Error: {e}")

        time.sleep(2)

except KeyboardInterrupt:
    print("\n" + "=" * 60)
    print("Simulator stopped by user")
    print(f"Total iterations: {iteration}")
    print(f"Normal: {normal_count} | Warning: {warning_count} | Critical: {critical_count}")
    print("=" * 60)
except Exception as e:
    print(f"\n✗ Fatal error: {e}")
    sys.exit(1)
