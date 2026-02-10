from flask import Flask,request,jsonify
from flask_cors import CORS
from db import init_db,get_connection

app=Flask(__name__)
CORS(app)
init_db()

@app.route("/api/alerts",methods=["POST"])
def alert():
    d=request.json
    c=get_connection().cursor()
    c.execute("INSERT INTO alerts(patient_id,alert_type,hr,spo2,temp,acc_mag,timestamp) VALUES(?,?,?,?,?,?,?)",
    (d["patient_id"],d["type"],d["hr"],d["spo2"],d["temp"],d["acc_mag"],d["timestamp"]))
    c.connection.commit()
    return jsonify(ok=True)

@app.route("/api/health",methods=["POST"])
def health():
    d=request.json
    c=get_connection().cursor()
    c.execute("""INSERT OR REPLACE INTO patient_health VALUES(?,?,?,?,?,?,?)""",
    (d["patient_id"],d["status"],d["hr"],d["spo2"],d["temp"],d["acc_mag"],d["timestamp"]))
    c.connection.commit()
    return jsonify(ok=True)

@app.route("/api/alerts",methods=["GET"])
def get_alerts():
    c=get_connection().cursor()
    rows=c.execute("SELECT * FROM alerts ORDER BY timestamp DESC").fetchall()
    return jsonify([dict(zip(["id","patient_id","alert_type","hr","spo2","temp","acc_mag","timestamp"],r)) for r in rows])

@app.route("/api/patients",methods=["GET"])
def patients():
    c=get_connection().cursor()
    rows=c.execute("SELECT * FROM patient_health").fetchall()
    return jsonify([dict(zip(["patient_id","status","hr","spo2","temp","acc_mag","timestamp"],r)) for r in rows])

@app.route("/api/patients/<pid>/status")
def status(pid):
    c=get_connection().cursor()
    r=c.execute("SELECT status FROM patient_health WHERE patient_id=?",(pid,)).fetchone()
    return jsonify({"status":r[0] if r else "NORMAL"})

if __name__=="__main__":
    app.run(port=5000)
