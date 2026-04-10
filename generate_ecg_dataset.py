import pandas as pd
import numpy as np
import random

# Generate realistic ECG dataset with features
np.random.seed(42)

data = []

# Generate 200 samples
for i in range(200):
    # 70% Normal (label 0), 30% Abnormal (label 1)
    if random.random() < 0.7:
        # Normal ECG features
        mean = np.random.uniform(-0.1, 0.1)
        std = np.random.uniform(0.3, 0.6)
        min_val = np.random.uniform(-1.5, -0.8)
        max_val = np.random.uniform(0.8, 1.5)
        median = np.random.uniform(-0.05, 0.05)
        label = 0  # Normal
        
        # Normal vitals
        hr = np.random.randint(60, 100)
        spo2 = np.random.uniform(95, 99)
        temp = np.random.uniform(36.5, 37.5)
        acc_mag = np.random.uniform(0.8, 1.2)
    else:
        # Abnormal ECG features
        mean = np.random.uniform(-0.3, 0.3)
        std = np.random.uniform(0.7, 1.2)
        min_val = np.random.uniform(-2.5, -1.5)
        max_val = np.random.uniform(1.5, 2.5)
        median = np.random.uniform(-0.2, 0.2)
        label = 1  # Abnormal
        
        # Abnormal vitals
        hr = np.random.randint(150, 180)
        spo2 = np.random.uniform(88, 94)
        temp = np.random.uniform(37.6, 39.5)
        acc_mag = np.random.uniform(20, 25)
    
    data.append({
        'mean': mean,
        'std': std,
        'min': min_val,
        'max': max_val,
        'median': median,
        'label': label,
        'hr': hr,
        'spo2': round(spo2, 1),
        'temp': round(temp, 1),
        'acc_mag': round(acc_mag, 2)
    })

df = pd.DataFrame(data)
df.to_csv('patient_simulator/ecg_features.csv', index=False)
print(f"✓ Generated {len(df)} ECG samples")
print(f"✓ Normal samples: {len(df[df.label == 0])}")
print(f"✓ Abnormal samples: {len(df[df.label == 1])}")
print(f"✓ Saved to: patient_simulator/ecg_features.csv")
print("\nFirst 5 rows:")
print(df.head())
