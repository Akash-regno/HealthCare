import { useEffect, useState } from 'react'
import { Heart, Droplet, Thermometer, Activity, User, TrendingUp, Clock } from 'lucide-react'

interface Patient {
  patient_id: string
  status: string
  hr: number
  spo2: number
  temp: number
  acc_mag: number
  timestamp: number
}

const API = 'http://127.0.0.1:5000'

export default function Patients() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null)

  const fetchData = async () => {
    try {
      const response = await fetch(`${API}/api/patients`)
      const data = await response.json()
      setPatients(data)
      if (data.length > 0 && !selectedPatient) {
        setSelectedPatient(data[0])
      }
    } catch (error) {
      console.error('Error fetching patients:', error)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 3000)
    return () => clearInterval(interval)
  }, [])

  const getStatusClass = (status: string) => {
    if (status === 'CRITICAL') return 'critical'
    if (status === 'WARNING') return 'warning'
    return 'normal'
  }

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString()
  }

  const getVitalStatus = (value: number, type: string) => {
    if (type === 'hr') {
      if (value < 60 || value > 100) return 'abnormal'
      return 'normal'
    }
    if (type === 'spo2') {
      if (value < 95) return 'abnormal'
      return 'normal'
    }
    if (type === 'temp') {
      if (value < 36.5 || value > 37.5) return 'abnormal'
      return 'normal'
    }
    return 'normal'
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Patient Management</h1>
          <p className="subtitle">Monitor and manage all patients in real-time</p>
        </div>
        <div className="stats-summary">
          <div className="summary-item">
            <span className="summary-label">Total Patients</span>
            <span className="summary-value">{patients.length}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Critical</span>
            <span className="summary-value critical">{patients.filter(p => p.status === 'CRITICAL').length}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Normal</span>
            <span className="summary-value normal">{patients.filter(p => p.status === 'NORMAL').length}</span>
          </div>
        </div>
      </div>

      <div className="patients-layout">
        {/* Patient List */}
        <div className="patient-list-card card">
          <div className="card-header">
            <div className="card-header-content">
              <h2>All Patients</h2>
              <p className="card-subtitle">{patients.length} active</p>
            </div>
          </div>
          <div className="card-body">
            <div className="patient-list">
              {patients.map((patient) => (
                <div
                  key={patient.patient_id}
                  className={`patient-list-item ${selectedPatient?.patient_id === patient.patient_id ? 'active' : ''}`}
                  onClick={() => setSelectedPatient(patient)}
                >
                  <div className="patient-avatar large">{patient.patient_id.charAt(0)}</div>
                  <div className="patient-list-info">
                    <div className="patient-list-name">{patient.patient_id}</div>
                    <div className="patient-list-meta">
                      <span className={`status-dot ${getStatusClass(patient.status)}`}></span>
                      {patient.status}
                    </div>
                  </div>
                  <div className="patient-list-vitals">
                    <div className="vital-mini">
                      <Heart size={14} />
                      <span>{patient.hr}</span>
                    </div>
                    <div className="vital-mini">
                      <Droplet size={14} />
                      <span>{patient.spo2}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Patient Details */}
        {selectedPatient && (
          <div className="patient-details">
            <div className="card">
              <div className="card-header">
                <div className="patient-header">
                  <div className="patient-avatar xlarge">{selectedPatient.patient_id.charAt(0)}</div>
                  <div>
                    <h2>{selectedPatient.patient_id}</h2>
                    <div className="patient-status-row">
                      <span className={`status-pill ${getStatusClass(selectedPatient.status)}`}>
                        {selectedPatient.status}
                      </span>
                      <span className="patient-time">
                        <Clock size={14} />
                        Last updated: {formatTimestamp(selectedPatient.timestamp)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="card-body">
                <div className="vitals-grid">
                  <div className={`vital-card ${getVitalStatus(selectedPatient.hr, 'hr')}`}>
                    <div className="vital-icon heart">
                      <Heart size={24} />
                    </div>
                    <div className="vital-content">
                      <div className="vital-label">Heart Rate</div>
                      <div className="vital-value">
                        {selectedPatient.hr}
                        <span className="vital-unit">bpm</span>
                      </div>
                      <div className="vital-range">Normal: 60-100 bpm</div>
                      <div className="progress-bar">
                        <div className="progress-fill heart-fill" style={{width: `${Math.min(selectedPatient.hr / 200 * 100, 100)}%`}}></div>
                      </div>
                    </div>
                  </div>

                  <div className={`vital-card ${getVitalStatus(selectedPatient.spo2, 'spo2')}`}>
                    <div className="vital-icon oxygen">
                      <Droplet size={24} />
                    </div>
                    <div className="vital-content">
                      <div className="vital-label">Oxygen Saturation</div>
                      <div className="vital-value">
                        {selectedPatient.spo2}
                        <span className="vital-unit">%</span>
                      </div>
                      <div className="vital-range">Normal: 95-100%</div>
                      <div className="progress-bar">
                        <div className="progress-fill oxygen-fill" style={{width: `${selectedPatient.spo2}%`}}></div>
                      </div>
                    </div>
                  </div>

                  <div className={`vital-card ${getVitalStatus(selectedPatient.temp, 'temp')}`}>
                    <div className="vital-icon temp">
                      <Thermometer size={24} />
                    </div>
                    <div className="vital-content">
                      <div className="vital-label">Body Temperature</div>
                      <div className="vital-value">
                        {selectedPatient.temp}
                        <span className="vital-unit">°C</span>
                      </div>
                      <div className="vital-range">Normal: 36.5-37.5°C</div>
                      <div className="progress-bar">
                        <div className="progress-fill" style={{width: `${((selectedPatient.temp - 35) / 5) * 100}%`}}></div>
                      </div>
                    </div>
                  </div>

                  <div className="vital-card">
                    <div className="vital-icon activity">
                      <Activity size={24} />
                    </div>
                    <div className="vital-content">
                      <div className="vital-label">Movement Activity</div>
                      <div className="vital-value">
                        {selectedPatient.acc_mag.toFixed(2)}
                        <span className="vital-unit">g</span>
                      </div>
                      <div className="vital-range">Acceleration magnitude</div>
                      <div className="progress-bar">
                        <div className="progress-fill" style={{width: `${Math.min(selectedPatient.acc_mag / 30 * 100, 100)}%`}}></div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="patient-info-section">
                  <h3>Patient Information</h3>
                  <div className="info-grid">
                    <div className="info-item">
                      <User size={16} />
                      <div>
                        <div className="info-label">Patient ID</div>
                        <div className="info-value">{selectedPatient.patient_id}</div>
                      </div>
                    </div>
                    <div className="info-item">
                      <TrendingUp size={16} />
                      <div>
                        <div className="info-label">Current Status</div>
                        <div className="info-value">{selectedPatient.status}</div>
                      </div>
                    </div>
                    <div className="info-item">
                      <Clock size={16} />
                      <div>
                        <div className="info-label">Last Reading</div>
                        <div className="info-value">{formatTimestamp(selectedPatient.timestamp)}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  )
}
