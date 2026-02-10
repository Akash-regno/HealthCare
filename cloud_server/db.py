import sqlite3

DB_PATH = "healthcare.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Table for patient health status
    c.execute("""
        CREATE TABLE IF NOT EXISTS patient_health (
            patient_id TEXT PRIMARY KEY,
            status TEXT,
            hr INTEGER,
            spo2 REAL,
            temp REAL,
            acc_mag REAL,
            timestamp REAL
        )
    """)
    
    # Table for alerts
    c.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT,
            alert_type TEXT,
            hr INTEGER,
            spo2 REAL,
            temp REAL,
            acc_mag REAL,
            timestamp REAL
        )
    """)
    
    conn.commit()
    print("Database initialized successfully")
