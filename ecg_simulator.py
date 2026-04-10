import time
import pandas as pd
import requests
import random
import joblib
import sys
import numpy as np
from email_notification import EmailNotification

# Initialize email notification service
email_notifier = EmailNotification()

# Load ECG model
try:
    model = joblib.load("ecg_model.pkl")
    print("✓ ECG RandomForest model loaded successfully")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    sys.exit(1)

# Load ECG features data
try:
    df = pd.read_csv("patient_simulator/ecg_features.csv")
    print(f"✓ Loaded {len(df)} ECG feature records")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    sys.exit(1)

CLOUD_ALERT_API = "http://127.0.0.1:5000/api/alerts"
CLOUD_HEALTH_API = "http://127.0.0.1:5000/api/health"

print("=" * 60)
print("🏥 SMART HEALTHCARE MONITORING - ECG SIMULATOR")
print("=" * 60)
print("ECG-based anomaly detection with RandomForest")
print(f"Backend API: {CLOUD_HEALTH_API}")
print(f"Generating data every 2 seconds...")
print("=" * 60)

iteration = 0
normal_count = 0
abnormal_count = 0

try:
    for _, row in df.iterrows():
        iteration += 1
        
        # Extract ECG features
        ecg_features = [[row['mean'], row['std'], row['min'], row['max'], row['median']]]
        
        # Predict using ECG model
        prediction = model.predict(ecg_features)[0]
        
        # Get vitals from dataset
        hr = int(row['hr'])
        spo2 = float(row['spo2'])
        temp = float(row['temp'])
        acc = float(row['acc_mag'])
        
        # Determine status based on ECG prediction and vitals
        if prediction == 1:  # Abnormal ECG
            status = "CRITICAL"
            abnormal_count += 1
        elif hr > 140 or acc > 20:
            status = "CRITICAL"
            abnormal_count += 1
        elif hr > 100 or spo2 < 95:
            status = "WARNING"
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
                
                # Send email notification to doctor
                email_notifier.send_critical_alert(
                    patient_id=health["patient_id"],
                    status=status,
                    hr=hr,
                    spo2=spo2,
                    temp=temp,
                    acc_mag=acc
                )
                
                print(f"[{iteration:04d}] 🚨 CRITICAL (ECG Abnormal): HR={hr} bpm, SpO2={spo2}%, Temp={temp}°C, ACC={acc}g")
            elif status == "WARNING":
                print(f"[{iteration:04d}] ⚠️  WARNING: HR={hr} bpm, SpO2={spo2}%, Temp={temp}°C, ACC={acc}g")
            else:
                print(f"[{iteration:04d}] ✓ NORMAL (ECG Normal): HR={hr} bpm, SpO2={spo2}%, Temp={temp}°C, ACC={acc}g")
                
        except requests.exceptions.RequestException as e:
            print(f"[{iteration:04d}] ✗ Connection Error: {e}")
        except Exception as e:
            print(f"[{iteration:04d}] ✗ Error: {e}")

        time.sleep(2)

except KeyboardInterrupt:
    print("\n" + "=" * 60)
    print("ECG Simulator stopped by user")
    print(f"Total iterations: {iteration}")
    print(f"Normal: {normal_count} | Abnormal: {abnormal_count}")
    print("=" * 60)
except Exception as e:
    print(f"\n✗ Fatal error: {e}")
    sys.exit(1)
