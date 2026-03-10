import sqlite3
import os

DB_PATH = "healthcare.db"

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

def init_db():
    """Initialize database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for patient health status
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_health (
            patient_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            hr INTEGER NOT NULL,
            spo2 REAL NOT NULL,
            temp REAL NOT NULL,
            acc_mag REAL NOT NULL,
            timestamp REAL NOT NULL
        )
    """)
    
    # Table for alerts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            hr INTEGER NOT NULL,
            spo2 REAL NOT NULL,
            temp REAL NOT NULL,
            acc_mag REAL NOT NULL,
            timestamp REAL NOT NULL
        )
    """)
    
    # Create indexes for better query performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_alerts_timestamp 
        ON alerts(timestamp DESC)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_alerts_patient 
        ON alerts(patient_id)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_health_status 
        ON patient_health(status)
    """)
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully")
    print(f"✓ Database location: {os.path.abspath(DB_PATH)}")

def clear_old_alerts(days=7):
    """Clear alerts older than specified days"""
    import time
    conn = get_connection()
    cursor = conn.cursor()
    cutoff_time = time.time() - (days * 24 * 60 * 60)
    cursor.execute("DELETE FROM alerts WHERE timestamp < ?", (cutoff_time,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted

if __name__ == "__main__":
    init_db()
    print("Database setup complete!")
