import wfdb
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# load ECG record
record_path = r"E:\6th sem\fog\project\dataset\100"
record = wfdb.rdrecord(record_path)

signal = record.p_signal[:,0]
fs = record.fs

# detect R-peaks
peaks,_ = find_peaks(signal, distance=fs*0.6)

# RR interval in seconds
rr = np.diff(peaks) / fs

# heart rate in bpm
hr = 60 / rr

# keep realistic range
hr = hr[(hr>40)&(hr<180)]

df = pd.DataFrame({
    "hr":hr[:200],
    "spo2":98,
    "temp":36.8,
    "acc_mag":1.0
})

df.to_csv("mitbih_hr.csv",index=False)

print("CSV created: mitbih_hr.csv")
