import { BrowserRouter, Routes, Route, Link, useLocation, Navigate } from 'react-router-dom'
import { Activity, Users, Bell, LogOut } from 'lucide-react'
import { useState, useEffect } from 'react'
import Dashboard from './pages/Dashboard'
import Patients from './pages/Patients'
import Alerts from './pages/Alerts'
import Login from './pages/Login'
import Home from './pages/Home'
import './App.css'

const API = 'http://127.0.0.1:5000'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />
}

function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const [isConnected, setIsConnected] = useState(true)
  const [alertCount, setAlertCount] = useState(0)
  const [showLogoutModal, setShowLogoutModal] = useState(false)
  const userName = localStorage.getItem('userName') || 'User'

  const handleLogout = () => {
    setShowLogoutModal(true)
  }

  const confirmLogout = () => {
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('userName')
    window.location.href = '/login'
  }

  const cancelLogout = () => {
    setShowLogoutModal(false)
  }

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch(`${API}/api/alerts`)
        const data = await response.json()
        setAlertCount(data.length)
        setIsConnected(true)
      } catch (error) {
        setIsConnected(false)
      }
    }

    checkConnection()
    const interval = setInterval(checkConnection, 5000)
    return () => clearInterval(interval)
  }, [])

  const getPageTitle = () => {
    if (location.pathname === '/dashboard') return 'Patient Monitoring Dashboard'
    if (location.pathname === '/patients') return 'Patient Management'
    if (location.pathname === '/alerts') return 'Alert Management'
    return 'Dashboard'
  }

  const getPageSubtitle = () => {
    if (location.pathname === '/dashboard') return 'Real-time fog computing based healthcare system'
    if (location.pathname === '/patients') return 'Monitor and manage all patients'
    if (location.pathname === '/alerts') return 'View and manage critical alerts'
    return ''
  }

  return (
    <>
      <div className="dashboard">
        {/* Sidebar */}
        <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <Activity className="logo-icon" size={32} />
            <span>HealthCare</span>
          </div>
        </div>
        
        <nav className="sidebar-nav">
          <Link to="/dashboard" className={`nav-item ${location.pathname === '/dashboard' ? 'active' : ''}`}>
            <Activity size={20} />
            <span>Dashboard</span>
          </Link>
          <Link to="/patients" className={`nav-item ${location.pathname === '/patients' ? 'active' : ''}`}>
            <Users size={20} />
            <span>Patients</span>
          </Link>
          <Link to="/alerts" className={`nav-item ${location.pathname === '/alerts' ? 'active' : ''}`}>
            <Bell size={20} />
            <span>Alerts</span>
            {alertCount > 0 && <span className="nav-badge">{alertCount}</span>}
          </Link>
        </nav>

        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="user-avatar">{userName.charAt(0).toUpperCase()}</div>
            <div className="user-info">
              <div className="user-name">{userName}</div>
              <button onClick={handleLogout} className="logout-btn">
                <LogOut size={14} />
                <span>Logout</span>
              </button>
            </div>
          </div>
          <div className={`connection-badge ${isConnected ? 'connected' : 'disconnected'}`}>
            <div className="pulse-dot"></div>
            <span>{isConnected ? 'Connected' : 'Offline'}</span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content page-transition">
        {children}
      </main>
    </div>

    {/* Logout Confirmation Modal */}
    {showLogoutModal && (
      <div className="modal-overlay" onClick={cancelLogout}>
        <div className="logout-modal" onClick={(e) => e.stopPropagation()}>
          <div className="logout-modal-icon">
            <LogOut size={32} />
          </div>
          <h2>Confirm Logout</h2>
          <p>Are you sure you want to logout? You will need to sign in again to access the dashboard.</p>
          <div className="logout-modal-actions">
            <button className="logout-cancel-btn" onClick={cancelLogout}>
              Cancel
            </button>
            <button className="logout-confirm-btn" onClick={confirmLogout}>
              Logout
            </button>
          </div>
        </div>
      </div>
    )}
  </>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Home />} />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </ProtectedRoute>
        } />
        <Route path="/patients" element={
          <ProtectedRoute>
            <Layout>
              <Patients />
            </Layout>
          </ProtectedRoute>
        } />
        <Route path="/alerts" element={
          <ProtectedRoute>
            <Layout>
              <Alerts />
            </Layout>
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default App
