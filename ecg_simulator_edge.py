"""
🚀 SMART HEALTHCARE MONITORING - ECG SIMULATOR
Edge Computing Version using Edge Impulse SDK

Simulates realistic patient data with on-device ECG anomaly detection.
Uses Edge Impulse for edge-deployed machine learning inference.
"""

import time
import pandas as pd
import requests
import sys
import numpy as np
from email_notification import EmailNotification
from edge_impulse_model import initialize_edge_model, predict_ecg_anomaly

# ============================================================================
# EDGE COMPUTING INITIALIZATION
# ============================================================================

print("=" * 70)
print("🏥 SMART HEALTHCARE MONITORING - ECG SIMULATOR (EDGE VERSION)")
print("=" * 70)
print("🚀 Initializing Edge Impulse ECG Detection Model...")

try:
    edge_model, edge_manager = initialize_edge_model()
    print("✓ Edge Impulse model initialized successfully")
except Exception as e:
    print(f"⚠️  Edge model initialization warning: {e}")
    print("   System will use fallback inference mode")

# Initialize email notification service
email_notifier = EmailNotification()

# ============================================================================
# LOAD REALISTIC ECG DATASET
# ============================================================================

print("\n📊 Loading realistic ECG dataset...")

try:
    # Load the main dataset with ECG features and labels
    df = pd.read_csv("ecg_dataset_realistic.csv")
    print(f"✓ Loaded {len(df)} ECG records from ecg_dataset_realistic.csv")
except Exception as e:
    print(f"✗ Error loading ecg_dataset_realistic.csv: {e}")
    sys.exit(1)

# Optional: Load supplementary features if available
try:
    df_features = pd.read_csv("patient_simulator/ecg_features.csv")
    print(f"✓ Loaded supplementary features from patient_simulator/ecg_features.csv")
    has_features = True
except FileNotFoundError:
    print("⚠️  Supplementary features file not found, using main dataset only")
    has_features = False

# ============================================================================
# CONFIGURATION
# ============================================================================

CLOUD_ALERT_API = "http://127.0.0.1:5000/api/alerts"
CLOUD_HEALTH_API = "http://127.0.0.1:5000/api/health"
UPDATE_INTERVAL = 2  # seconds

# Feature columns in the dataset
FEATURE_COLUMNS = ['mean', 'std', 'min', 'max', 'median']

print(f"\n⚙️  Configuration:")
print(f"  Backend API: {CLOUD_HEALTH_API}")
print(f"  Alert API: {CLOUD_ALERT_API}")
print(f"  Data update interval: {UPDATE_INTERVAL}s")
print(f"  Edge Computing Model: Edge Impulse SDK")

print("\n" + "=" * 70)
print("Starting ECG simulation with on-device anomaly detection...")
print("=" * 70 + "\n")

# ============================================================================
# MAIN SIMULATION LOOP
# ============================================================================

iteration = 0
normal_count = 0
abnormal_count = 0
critical_count = 0
warning_count = 0
edge_predictions = []

try:
    for idx, row in df.iterrows():
        iteration += 1
        
        # ====================================================================
        # EDGE COMPUTING: On-device ECG Feature Extraction
        # ====================================================================
        
        # Extract ECG features (already computed in dataset)
        ecg_features = {col: float(row[col]) for col in FEATURE_COLUMNS}
        
        # Get ground truth label from dataset (0=Normal, 1=Abnormal)
        ground_truth_label = int(row['label']) if 'label' in row else 0
        
        # ====================================================================
        # EDGE COMPUTING: On-device Inference
        # ====================================================================
        
        # Run Edge Impulse model inference ON DEVICE
        ei_prediction, ei_confidence = predict_ecg_anomaly(
            ecg_features['mean'],
            ecg_features['std'],
            ecg_features['min'],
            ecg_features['max'],
            ecg_features['median']
        )
        
        # Convert prediction to binary (0=Normal, 1=Abnormal)
        edge_prediction = 1 if ei_prediction == "Abnormal" else 0
        edge_predictions.append({
            'iteration': iteration,
            'prediction': edge_prediction,
            'confidence': ei_confidence,
            'ground_truth': ground_truth_label
        })
        
        # ====================================================================
        # VITAL SIGNS EXTRACTION
        # ====================================================================
        
        # Get vital signs - try from supplementary features first
        if has_features and idx < len(df_features):
            row_features = df_features.iloc[idx]
            hr = int(row_features.get('hr', 80))
            spo2 = float(row_features.get('spo2', 96.0))
            temp = float(row_features.get('temp', 37.0))
            acc_mag = float(row_features.get('acc_mag', 1.0))
        else:
            # Generate realistic vital signs based on ECG features
            # From the dataset analysis: abnormal ECGs tend to have higher HR
            if edge_prediction == 1:
                hr = np.random.randint(140, 180)
                spo2 = np.random.uniform(88, 94)
                temp = np.random.uniform(37.5, 39.5)
                acc_mag = np.random.uniform(15, 25)
            else:
                hr = np.random.randint(60, 100)
                spo2 = np.random.uniform(95, 99)
                temp = np.random.uniform(36.5, 37.5)
                acc_mag = np.random.uniform(0.5, 2.0)
        
        # ====================================================================
        # STATUS DETERMINATION (Multi-factor Assessment)
        # ====================================================================
        
        status = "NORMAL"
        
        # Factor 1: Edge Impulse ECG Detection
        if edge_prediction == 1:
            status = "CRITICAL"
            abnormal_count += 1
        # Factor 2: Vital signs thresholds
        elif hr > 140 or acc_mag > 20:
            status = "CRITICAL"
            abnormal_count += 1
        elif hr > 100 or spo2 < 95:
            status = "WARNING"
            warning_count += 1
        else:
            status = "NORMAL"
            normal_count += 1
        
        if status == "CRITICAL":
            critical_count += 1
        
        # ====================================================================
        # PREPARE PATIENT DATA
        # ====================================================================
        
        health_data = {
            "patient_id": "P001",
            "status": status,
            "hr": int(hr),
            "spo2": float(spo2),
            "temp": float(temp),
            "acc_mag": float(acc_mag),
            "timestamp": time.time(),
            "edge_prediction": ei_prediction,
            "edge_confidence": float(ei_confidence),
            "model_source": "Edge Impulse SDK"
        }
        
        # ====================================================================
        # SEND TO CLOUD & ALERTS
        # ====================================================================
        
        try:
            # Send health update to cloud
            response = requests.post(CLOUD_HEALTH_API, json=health_data, timeout=5)
            
            if status == "CRITICAL":
                # Send alert to cloud
                alert_data = health_data.copy()
                alert_data["type"] = "CRITICAL"
                requests.post(CLOUD_ALERT_API, json=alert_data, timeout=5)
                
                # Send email notification to doctor
                email_notifier.send_critical_alert(
                    patient_id=health_data["patient_id"],
                    status=status,
                    hr=int(hr),
                    spo2=spo2,
                    temp=temp,
                    acc_mag=acc_mag
                )
                
                print(f"[{iteration:04d}] 🚨 CRITICAL - Edge: {ei_prediction} ({ei_confidence:.1%})")
                print(f"         HR={int(hr)} bpm, SpO2={spo2:.1f}%, Temp={temp:.1f}°C, ACC={acc_mag:.2f}g")
            
            elif status == "WARNING":
                print(f"[{iteration:04d}] ⚠️  WARNING - Edge: {ei_prediction} ({ei_confidence:.1%})")
                print(f"         HR={int(hr)} bpm, SpO2={spo2:.1f}%, Temp={temp:.1f}°C")
            
            else:
                # Normal status with less verbose output
                if iteration % 10 == 0:  # Log every 10th normal reading
                    print(f"[{iteration:04d}] ✓ NORMAL  - Edge: {ei_prediction} ({ei_confidence:.1%})")
                    print(f"         HR={int(hr)} bpm, SpO2={spo2:.1f}%, Temp={temp:.1f}°C")
        
        except requests.exceptions.RequestException as e:
            print(f"[{iteration:04d}] ✗ Connection Error: {e}")
        except Exception as e:
            print(f"[{iteration:04d}] ✗ Error: {e}")
        
        # Wait before next reading
        time.sleep(UPDATE_INTERVAL)

except KeyboardInterrupt:
    print("\n" + "=" * 70)
    print("🛑 ECG Simulator stopped by user")
    print("=" * 70)

except Exception as e:
    print(f"\n✗ Fatal error: {e}")
    sys.exit(1)

finally:
    # ========================================================================
    # PRINT STATISTICS
    # ========================================================================
    
    print("\n" + "=" * 70)
    print("📊 SIMULATION SUMMARY")
    print("=" * 70)
    print(f"Total iterations: {iteration}")
    print(f"Normal readings:  {normal_count} ({100*normal_count/max(1,iteration):.1f}%)")
    print(f"Warning readings: {warning_count} ({100*warning_count/max(1,iteration):.1f}%)")
    print(f"Critical alerts:  {abnormal_count} ({100*abnormal_count/max(1,iteration):.1f}%)")
    
    if edge_predictions:
        print(f"\n🚀 EDGE IMPULSE MODEL PERFORMANCE:")
        correct = sum(1 for p in edge_predictions if p['prediction'] == p['ground_truth'])
        accuracy = correct / len(edge_predictions) * 100
        print(f"Accuracy vs Dataset Labels: {accuracy:.1f}%")
    
    print(f"\n🏥 Backend Status:")
    print(f"Cloud API: {CLOUD_HEALTH_API}")
    print(f"Alert API: {CLOUD_ALERT_API}")
    
    print("\n" + "=" * 70)
