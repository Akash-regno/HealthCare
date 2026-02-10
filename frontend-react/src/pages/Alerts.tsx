import { useEffect, useState } from 'react'
import { AlertTriangle, Heart, Droplet, Thermometer, Activity, Clock, Filter, Search, ArrowUp, ArrowDown } from 'lucide-react'

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

const API = 'http://127.0.0.1:5000'

export default function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [filteredAlerts, setFilteredAlerts] = useState<Alert[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState('all')
  const [showScrollTop, setShowScrollTop] = useState(false)
  const [showScrollBottom, setShowScrollBottom] = useState(true)

  const fetchData = async () => {
    try {
      const response = await fetch(`${API}/api/alerts`)
      const data = await response.json()
      setAlerts(data)
      setFilteredAlerts(data)
    } catch (error) {
      console.error('Error fetching alerts:', error)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 3000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    let filtered = alerts

    if (searchTerm) {
      filtered = filtered.filter(alert =>
        alert.patient_id.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(alert => alert.alert_type === filterType)
    }

    setFilteredAlerts(filtered)
  }, [searchTerm, filterType, alerts])

  // Handle scroll to show/hide buttons
  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.scrollY
      const scrollHeight = document.documentElement.scrollHeight
      const clientHeight = window.innerHeight
      
      setShowScrollTop(scrollTop > 400)
      setShowScrollBottom(scrollTop + clientHeight < scrollHeight - 100)
    }

    window.addEventListener('scroll', handleScroll)
    handleScroll() // Initial check
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const scrollToBottom = () => {
    window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' })
  }

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString()
  }

  const getTimeAgo = (timestamp: number) => {
    const seconds = Math.floor(Date.now() / 1000 - timestamp)
    if (seconds < 60) return `${seconds}s ago`
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
    return `${Math.floor(seconds / 86400)}d ago`
  }

  const getSeverityClass = (alert: Alert) => {
    if (alert.hr > 150 || alert.acc_mag > 20) return 'severe'
    if (alert.hr > 120 || alert.acc_mag > 15) return 'high'
    return 'medium'
  }

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Alert Management</h1>
          <p className="subtitle">Monitor and manage all critical alerts</p>
        </div>
        <div className="stats-summary">
          <div className="summary-item">
            <span className="summary-label">Total Alerts</span>
            <span className="summary-value">{alerts.length}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Last Hour</span>
            <span className="summary-value">{alerts.filter(a => Date.now() / 1000 - a.timestamp < 3600).length}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Critical</span>
            <span className="summary-value critical">{alerts.filter(a => a.alert_type === 'CRITICAL').length}</span>
          </div>
        </div>
      </div>

      <div className="alerts-page-layout">
        {/* Filters */}
        <div className="card filters-card">
          <div className="card-body">
            <div className="filters-row">
              <div className="search-box">
                <Search size={18} />
                <input
                  type="text"
                  placeholder="Search by patient ID..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <div className="filter-group">
                <Filter size={18} />
                <select value={filterType} onChange={(e) => setFilterType(e.target.value)}>
                  <option value="all">All Types</option>
                  <option value="CRITICAL">Critical Only</option>
                  <option value="WARNING">Warning Only</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Alerts List */}
        <div className="card">
          <div className="card-header">
            <div className="card-header-content">
              <h2>Alert History</h2>
              <p className="card-subtitle">{filteredAlerts.length} alert(s) found</p>
            </div>
          </div>
          <div className="card-body">
            {filteredAlerts.length === 0 ? (
              <div className="empty-state">
                <AlertTriangle size={48} className="empty-icon" />
                <p>No alerts found</p>
                <span className="empty-subtitle">Try adjusting your filters</span>
              </div>
            ) : (
              <div className="alerts-table-container">
                <table className="alerts-table">
                  <thead>
                    <tr>
                      <th>Alert ID</th>
                      <th>Patient</th>
                      <th>Type</th>
                      <th>Severity</th>
                      <th>Heart Rate</th>
                      <th>SpO₂</th>
                      <th>Temperature</th>
                      <th>Movement</th>
                      <th>Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredAlerts.map((alert) => (
                      <tr key={alert.id} className={`alert-row ${getSeverityClass(alert)}`}>
                        <td>
                          <div className="alert-id">
                            <AlertTriangle size={16} />
                            #{alert.id}
                          </div>
                        </td>
                        <td>
                          <div className="patient-cell-mini">
                            <div className="patient-avatar small">{alert.patient_id.charAt(0)}</div>
                            <span className="patient-name-mini">{alert.patient_id}</span>
                          </div>
                        </td>
                        <td>
                          <span className="alert-type-badge">{alert.alert_type}</span>
                        </td>
                        <td>
                          <span className={`severity-badge ${getSeverityClass(alert)}`}>
                            {getSeverityClass(alert).toUpperCase()}
                          </span>
                        </td>
                        <td>
                          <div className="vital-cell">
                            <Heart size={14} className={alert.hr > 140 ? 'text-danger' : ''} />
                            <span className={alert.hr > 140 ? 'text-danger' : ''}>{alert.hr} bpm</span>
                          </div>
                        </td>
                        <td>
                          <div className="vital-cell">
                            <Droplet size={14} className={alert.spo2 < 95 ? 'text-warning' : ''} />
                            <span className={alert.spo2 < 95 ? 'text-warning' : ''}>{alert.spo2}%</span>
                          </div>
                        </td>
                        <td>
                          <div className="vital-cell">
                            <Thermometer size={14} />
                            <span>{alert.temp}°C</span>
                          </div>
                        </td>
                        <td>
                          <div className="vital-cell">
                            <Activity size={14} className={alert.acc_mag > 20 ? 'text-danger' : ''} />
                            <span className={alert.acc_mag > 20 ? 'text-danger' : ''}>{alert.acc_mag.toFixed(2)}</span>
                          </div>
                        </td>
                        <td>
                          <div className="time-cell">
                            <Clock size={14} />
                            <div>
                              <div className="time-ago">{getTimeAgo(alert.timestamp)}</div>
                              <div className="time-full">{formatTimestamp(alert.timestamp)}</div>
                            </div>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>

        {/* Alert Statistics */}
        <div className="alert-stats-grid">
          <div className="stat-card-small">
            <div className="stat-icon-small severe">
              <AlertTriangle size={20} />
            </div>
            <div>
              <div className="stat-label-small">Severe Alerts</div>
              <div className="stat-value-small">{alerts.filter(a => getSeverityClass(a) === 'severe').length}</div>
            </div>
          </div>
          <div className="stat-card-small">
            <div className="stat-icon-small high">
              <AlertTriangle size={20} />
            </div>
            <div>
              <div className="stat-label-small">High Priority</div>
              <div className="stat-value-small">{alerts.filter(a => getSeverityClass(a) === 'high').length}</div>
            </div>
          </div>
          <div className="stat-card-small">
            <div className="stat-icon-small medium">
              <AlertTriangle size={20} />
            </div>
            <div>
              <div className="stat-label-small">Medium Priority</div>
              <div className="stat-value-small">{alerts.filter(a => getSeverityClass(a) === 'medium').length}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Buttons */}
      <div className="scroll-buttons">
        {showScrollTop && (
          <button className="scroll-btn scroll-to-top" onClick={scrollToTop}>
            <ArrowUp size={20} />
          </button>
        )}
        {showScrollBottom && (
          <button className="scroll-btn scroll-to-bottom" onClick={scrollToBottom}>
            <ArrowDown size={20} />
          </button>
        )}
      </div>
    </>
  )
}
