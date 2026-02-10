# 🏥 Fog-Based Smart Healthcare Monitoring System

## 📌 Description

This project implements a **Fog Computing–based Smart Healthcare Monitoring System** that performs **real-time patient vital analysis and anomaly detection at the edge (fog layer)** instead of relying entirely on cloud processing.

Patient vital signs are simulated and transmitted using MQTT. A fog node processes this data locally using a Machine Learning model to classify patients as **NORMAL or CRITICAL**. Only alerts and summarized data are sent to the cloud backend for visualization.

This architecture reduces latency, preserves patient privacy, and enables offline operation during network failures.

---

## 🚀 Key Features

* Real-time patient vital simulation
* Fog-layer Machine Learning inference
* Local anomaly detection (Normal / Critical)
* MQTT-based data streaming
* Flask REST backend
* Web-based monitoring dashboard
* Lightweight SQLite database
* Reduced cloud dependency
* Privacy-preserving edge processing

---

## 🧠 System Architecture

```
Patient Simulator → MQTT Broker → Fog Node (ML) → Flask Backend → Web Dashboard
```

---

## 🧰 Tech Stack

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript

### Fog Layer

* Python 3
* Scikit-learn (ML model)
* Paho-MQTT

### Backend / Cloud Layer

* Python Flask (REST API)
* SQLite (local database)

### Communication

* MQTT (Eclipse Mosquitto)
* HTTP REST APIs

### Machine Learning

* Scikit-learn
* MIT-BIH derived dataset

### Infrastructure

* Mosquitto MQTT Broker

---

## 📂 Project Structure

```
Smart-Healthcare-Monitoring-Dashboard/
│
├── patient_simulator/
│   └── simulator.py
│
├── fog_node/
│   └── fog.py
│
├── backend/
│   └── app.py
│
├── frontend/
│   └── index.html
│
├── train_model.py
├── split_dataset.py
├── add_timestamp.py
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/anjaneyasahu0502/Smart-Healthcare-Monitoring-Dashboard.git
cd Smart-Healthcare-Monitoring-Dashboard
```

---

### 2. Install Python dependencies

```bash
pip install flask paho-mqtt scikit-learn pandas joblib requests
```

---

### 3. Install Mosquitto MQTT

Download from:

[https://mosquitto.org/download/](https://mosquitto.org/download/)

Ensure `mosquitto` works in terminal.

---

## ▶️ How To Run (IMPORTANT ORDER)

Open **four terminals**

---

### Terminal 1 — Start MQTT Broker

```bash
mosquitto
```

---

### Terminal 2 — Start Flask Backend

```bash
cd backend
python app.py
```

---

### Terminal 3 — Start Fog Node

```bash
cd fog_node
python fog.py
```

---

### Terminal 4 — Start Patient Simulator

```bash
python patient_simulator/simulator.py
```

---

## 🌐 Open Dashboard

Open:

```
frontend/index.html
```

in your browser.

---

## ✅ Output

* Live patient vitals
* NORMAL / CRITICAL classification
* Alert table for critical patients
* Continuous real-time updates

---

## 📊 Machine Learning

* Algorithm: Isolation Forest / Anomaly Detection
* Input Features:

  * Heart Rate
  * SpO₂
  * Temperature
  * Acceleration Magnitude

Fog node performs inference locally and forwards only alerts.

---

## 🎓 Academic Purpose

This project demonstrates:

* Fog Computing
* Edge intelligence
* Real-time healthcare analytics
* Privacy-preserving ML
* Distributed system design

Designed for **Fog & Edge Computing coursework**.

---

## 📜 License

MIT License

---

## 👤 Author

Anjaneya Sahu
B.Tech CSE

---