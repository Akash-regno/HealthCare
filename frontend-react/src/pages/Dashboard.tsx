import { useEffect, useState } from 'react'
import { Heart, Droplet, Thermometer, AlertTriangle, CheckCircle, Users, TrendingUp } from 'lucide-react'
import VitalChart from '../components/VitalChart'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'

interface Patient {
  patient_id: string
  status: string
  hr: number
  spo2: number
  temp: number
  acc_mag: number
  timestamp: number
}

interface Alert {
  id: number
  patient_id: string
  alert_type: string
  hr: number
  spo2: number
  temp: number
  acc_mag: number
  timestamp: number
}

interface VitalHistory {
  time: string
  value: number
}

const API = 'http://127.0.0.1:5000'

export default function Dashboard() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [patientStatus, setPatientStatus] = useState('Loading...')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // Vital history for charts - Load from localStorage on mount
  const [hrHistory, setHrHistory] = useState<VitalHistory[]>(() => {
    const saved = localStorage.getItem('hrHistory')
    return saved ? JSON.parse(saved) : []
  })
  const [spo2History, setSpo2History] = useState<VitalHistory[]>(() => {
    const saved = localStorage.getItem('spo2History')
    return saved ? JSON.parse(saved) : []
  })
  const [tempHistory, setTempHistory] = useState<VitalHistory[]>(() => {
    const saved = localStorage.getItem('tempHistory')
    return saved ? JSON.parse(saved) : []
  })

  // Save to localStorage whenever history changes
  useEffect(() => {
    localStorage.setItem('hrHistory', JSON.stringify(hrHistory))
  }, [hrHistory])

  useEffect(() => {
    localStorage.setItem('spo2History', JSON.stringify(spo2History))
  }, [spo2History])

  useEffect(() => {
    localStorage.setItem('tempHistory', JSON.stringify(tempHistory))
  }, [tempHistory])
  const fetchData = async () => {
    try {
      const [patientsRes, alertsRes, statusRes] = await Promise.all([
        fetch(`${API}/api/patients`),
        fetch(`${API}/api/alerts`),
        fetch(`${API}/api/patients/P001/status`)
      ])

      if (!patientsRes.ok || !alertsRes.ok || !statusRes.ok) {
        throw new Error('Failed to fetch data from server')
      }

      const patientsData = await patientsRes.json()
      const alertsData = await alertsRes.json()
      const statusData = await statusRes.json()

      setPatients(patientsData)
      setAlerts(alertsData)
      setPatientStatus(statusData.status)
      
      // Update vital history
      if (patientsData.length > 0) {
        const currentPatient = patientsData[0]
        const now = new Date()
        const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
        
        console.log('[Dashboard] Patient data:', currentPatient)
        console.log('[Dashboard] Time:', timeStr)
        
        setHrHistory(prev => {
          const newData = [...prev, { time: timeStr, value: currentPatient.hr }]
          const result = newData.slice(-20)
          console.log('[Dashboard] HR History updated:', result.length, 'points', result)
          return result
        })
        setSpo2History(prev => {
          const newData = [...prev, { time: timeStr, value: currentPatient.spo2 }]
          const result = newData.slice(-20)
          console.log('[Dashboard] SpO2 History updated:', result.length, 'points')
          return result
        })
        setTempHistory(prev => {
          const newData = [...prev, { time: timeStr, value: currentPatient.temp }]
          const result = newData.slice(-20)
          console.log('[Dashboard] Temp History updated:', result.length, 'points')
          return result
        })
      } else {
        console.log('[Dashboard] No patient data received')
      }
      
      setError(null)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching data:', error)
      setError('Unable to connect to the server. Please check if the backend is running.')
      setLoading(false)
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

  const currentPatient = patients.find(p => p.patient_id === 'P001')

  if (loading) {
    return <LoadingSpinner />
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchData} />
  }

  return (
    <>
      {/* Page Header */}
      <div className="page-header">
        <div>
          <h1>Patient Monitoring Dashboard</h1>
          <p className="subtitle">Real-time fog computing based healthcare system</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-container">
        <div className={`stat-card ${getStatusClass(patientStatus)}`}>
          <div className="stat-card-header">
            <div className={`stat-icon-wrapper status-icon ${getStatusClass(patientStatus)}`}>
              {patientStatus === 'CRITICAL' ? <AlertTriangle size={24} /> : <CheckCircle size={24} />}
            </div>
            <span className="stat-label">Patient Status</span>
          </div>
          <div className="stat-value-large">{patientStatus}</div>
          <div className="stat-footer">Patient P001</div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <div className="stat-icon-wrapper heart">
              <Heart size={24} />
            </div>
            <span className="stat-label">Heart Rate</span>
          </div>
          <div className="stat-value-large">
            {currentPatient?.hr || '--'}
            <span className="stat-unit">bpm</span>
          </div>
          <div className="stat-footer">
            <div className="progress-bar">
              <div className="progress-fill heart-fill" style={{width: `${Math.min((currentPatient?.hr || 0) / 200 * 100, 100)}%`}}></div>
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <div className="stat-icon-wrapper oxygen">
              <Droplet size={24} />
            </div>
            <span className="stat-label">Oxygen Level</span>
          </div>
          <div className="stat-value-large">
            {currentPatient?.spo2 || '--'}
            <span className="stat-unit">%</span>
          </div>
          <div className="stat-footer">
            <div className="progress-bar">
              <div className="progress-fill oxygen-fill" style={{width: `${currentPatient?.spo2 || 0}%`}}></div>
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-card-header">
            <div className="stat-icon-wrapper temp">
              <Thermometer size={24} />
            </div>
            <span className="stat-label">Temperature</span>
          </div>
          <div className="stat-value-large">
            {currentPatient?.temp || '--'}
            <span className="stat-unit">°C</span>
          </div>
          <div className="stat-footer">Normal: 36.5-37.5°C</div>
        </div>
      </div>

      {/* Vital Signs Trends */}
      <div className="charts-card">
        <div className="card">
          <div className="card-header">
            <div className="card-header-content">
              <h2><TrendingUp size={24} /> Vital Signs Trends</h2>
              <p className="card-subtitle">Real-time monitoring over last minute</p>
            </div>
          </div>
          <div className="card-body">
            <div className="charts-grid">
              <VitalChart data={hrHistory} color="#ef4444" label="Heart Rate (bpm)" />
              <VitalChart data={spo2History} color="#3b82f6" label="Oxygen Saturation (%)" />
              <VitalChart data={tempHistory} color="#f59e0b" label="Temperature (°C)" />
            </div>
          </div>
        </div>
      </div>

      {/* Content Grid */}
      <div className="content-grid">
        {/* Patients Table */}
        <div className="card">
          <div className="card-header">
            <div className="card-header-content">
              <h2>Active Patients</h2>
              <p className="card-subtitle">{patients.length} patient(s) monitored</p>
            </div>
          </div>
          <div className="card-body">
            {patients.length === 0 ? (
              <div className="empty-state">
                <Users size={48} className="empty-icon" />
                <p>No patient data available</p>
              </div>
            ) : (
              <div className="table-container">
                <table className="modern-table">
                  <thead>
                    <tr>
                      <th>Patient</th>
                      <th>Status</th>
                      <th>Heart Rate</th>
                      <th>SpO₂</th>
                      <th>Temperature</th>
                      <th>Movement</th>
                      <th>Last Update</th>
                    </tr>
                  </thead>
                  <tbody>
                    {patients.map((patient) => (
                      <tr key={patient.patient_id}>
                        <td>
                          <div className="patient-cell">
                            <div className="patient-avatar">{patient.patient_id.charAt(0)}</div>
                            <div className="patient-info">
                              <div className="patient-name">{patient.patient_id}</div>
                              <div className="patient-meta">Active</div>
                            </div>
                          </div>
                        </td>
                        <td>
                          <span className={`status-pill ${getStatusClass(patient.status)}`}>
                            {patient.status}
                          </span>
                        </td>
                        <td>
                          <div className="metric-cell">
                            <Heart size={16} className="metric-icon" />
                            <span>{patient.hr} bpm</span>
                          </div>
                        </td>
                        <td>
                          <div className="metric-cell">
                            <Droplet size={16} className="metric-icon" />
                            <span>{patient.spo2}%</span>
                          </div>
                        </td>
                        <td>
                          <div className="metric-cell">
                            <Thermometer size={16} className="metric-icon" />
                            <span>{patient.temp}°C</span>
                          </div>
                        </td>
                        <td>{patient.acc_mag.toFixed(2)}</td>
                        <td className="timestamp-cell">{formatTimestamp(patient.timestamp)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>

        {/* Alerts Panel */}
        <div className="card">
          <div className="card-header">
            <div className="card-header-content">
              <h2>Critical Alerts</h2>
              <p className="card-subtitle">{alerts.length} active alert(s)</p>
            </div>
          </div>
          <div className="card-body">
            {alerts.length === 0 ? (
              <div className="empty-state">
                <CheckCircle size={48} className="empty-icon success" />
                <p>No critical alerts</p>
                <span className="empty-subtitle">All patients stable</span>
              </div>
            ) : (
              <div className="alerts-container">
                {alerts.slice(0, 10).map((alert) => (
                  <div key={alert.id} className="alert-card">
                    <div className="alert-icon-wrapper">
                      <AlertTriangle size={20} />
                    </div>
                    <div className="alert-details">
                      <div className="alert-header-row">
                        <span className="alert-patient">{alert.patient_id}</span>
                        <span className="alert-badge">{alert.alert_type}</span>
                      </div>
                      <div className="alert-vitals-grid">
                        <div className="alert-vital">
                          <Heart size={14} />
                          <span>{alert.hr} bpm</span>
                        </div>
                        <div className="alert-vital">
                          <Droplet size={14} />
                          <span>{alert.spo2}%</span>
                        </div>
                        <div className="alert-vital">
                          <Thermometer size={14} />
                          <span>{alert.temp}°C</span>
                        </div>
                        <div className="alert-vital">
                          <AlertTriangle size={14} />
                          <span>{alert.acc_mag.toFixed(2)}</span>
                        </div>
                      </div>
                      <div className="alert-timestamp">{formatTimestamp(alert.timestamp)}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
