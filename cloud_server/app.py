from flask import Flask, request, jsonify
from flask_cors import CORS
from db import init_db, get_connection
import time

app = Flask(__name__)
CORS(app)
init_db()

@app.route("/api/alerts", methods=["POST"])
def create_alert():
    """Create a new alert"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alerts(patient_id, alert_type, hr, spo2, temp, acc_mag, timestamp) VALUES(?,?,?,?,?,?,?)",
            (data["patient_id"], data["type"], data["hr"], data["spo2"], data["temp"], data["acc_mag"], data["timestamp"])
        )
        conn.commit()
        conn.close()
        return jsonify({"ok": True, "message": "Alert created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/health", methods=["POST"])
def update_health():
    """Update patient health status"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT OR REPLACE INTO patient_health VALUES(?,?,?,?,?,?,?)""",
            (data["patient_id"], data["status"], data["hr"], data["spo2"], data["temp"], data["acc_mag"], data["timestamp"])
        )
        conn.commit()
        conn.close()
        return jsonify({"ok": True, "message": "Health status updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    """Get all alerts"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 100").fetchall()
        conn.close()
        
        alerts = [
            dict(zip(["id", "patient_id", "alert_type", "hr", "spo2", "temp", "acc_mag", "timestamp"], row))
            for row in rows
        ]
        return jsonify(alerts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/patients", methods=["GET"])
def get_patients():
    """Get all patients"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM patient_health ORDER BY timestamp DESC").fetchall()
        conn.close()
        
        patients = [
            dict(zip(["patient_id", "status", "hr", "spo2", "temp", "acc_mag", "timestamp"], row))
            for row in rows
        ]
        return jsonify(patients), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/patients/<pid>/status", methods=["GET"])
def get_patient_status(pid):
    """Get specific patient status"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT status FROM patient_health WHERE patient_id=?", (pid,)).fetchone()
        conn.close()
        
        if row:
            return jsonify({"patient_id": pid, "status": row[0]}), 200
        else:
            return jsonify({"patient_id": pid, "status": "NORMAL"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get dashboard statistics"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Total patients
        total_patients = cursor.execute("SELECT COUNT(*) FROM patient_health").fetchone()[0]
        
        # Critical patients
        critical_patients = cursor.execute("SELECT COUNT(*) FROM patient_health WHERE status='CRITICAL'").fetchone()[0]
        
        # Total alerts
        total_alerts = cursor.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
        
        # Alerts in last hour
        one_hour_ago = time.time() - 3600
        recent_alerts = cursor.execute("SELECT COUNT(*) FROM alerts WHERE timestamp > ?", (one_hour_ago,)).fetchone()[0]
        
        conn.close()
        
        return jsonify({
            "total_patients": total_patients,
            "critical_patients": critical_patients,
            "total_alerts": total_alerts,
            "recent_alerts": recent_alerts
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Smart Healthcare Monitoring API",
        "version": "1.0.0",
        "timestamp": time.time()
    }), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
