from sklearn.ensemble import IsolationForest
import numpy as np
import joblib

# fake NORMAL vital signs data
# [heart_rate, spo2, temperature, acc_magnitude]
X = np.column_stack((
    np.random.randint(60, 100, 500),
    np.random.uniform(95, 99, 500),
    np.random.uniform(36.5, 37.5, 500),
    np.random.uniform(0.5, 2.0, 500)
))

model = IsolationForest(
    contamination=0.1,
    random_state=42
)

model.fit(X)

joblib.dump(model, "model.pkl")

print("model.pkl created successfully")
