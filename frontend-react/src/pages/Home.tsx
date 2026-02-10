import { Activity, Heart, TrendingUp, Shield, Zap, Users } from 'lucide-react'
import { useNavigate, useLocation } from 'react-router-dom'
import Login from './Login'

export default function Home() {
  const navigate = useNavigate()
  const location = useLocation()
  const showLogin = location.pathname === '/login'

  return (
    <>
      <div className="home-container">
        {/* Header */}
        <header className="home-header">
          <div className="home-logo">
            <Activity size={32} />
            <span>HealthCare</span>
          </div>
          <button className="home-signin-btn" onClick={() => navigate('/login')}>
            Sign In
          </button>
        </header>

        {/* Hero Section */}
        <main className="home-main">
          <h1 className="home-title">
            Smart Healthcare
            <br />
            <span className="home-title-gradient">Monitoring System</span>
          </h1>

          <p className="home-description">
            Real-time fog computing based patient monitoring with advanced ML anomaly detection.
            Monitor vital signs, detect anomalies instantly, and save lives with cutting-edge technology.
          </p>

          <div className="home-actions">
            <button className="home-btn-primary" onClick={() => navigate('/login')}>
              Get Started
            </button>
            <button className="home-btn-secondary">
              Learn More
            </button>
          </div>

          {/* Stats */}
          <div className="home-stats">
            <div className="home-stat">
              <div className="home-stat-value">1000+</div>
              <div className="home-stat-label">Patients Monitored</div>
            </div>
            <div className="home-stat-divider"></div>
            <div className="home-stat">
              <div className="home-stat-value">24/7</div>
              <div className="home-stat-label">Real-time Monitoring</div>
            </div>
            <div className="home-stat-divider"></div>
            <div className="home-stat">
              <div className="home-stat-value">99.9%</div>
              <div className="home-stat-label">Uptime</div>
            </div>
          </div>

          {/* Features */}
          <div className="home-features">
            <div className="home-feature-card">
              <div className="feature-icon-wrapper heart">
                <Heart size={24} />
              </div>
              <h3>Real-time Vitals</h3>
              <p>Monitor heart rate, oxygen levels, temperature, and movement in real-time</p>
            </div>

            <div className="home-feature-card">
              <div className="feature-icon-wrapper ai">
                <TrendingUp size={24} />
              </div>
              <h3>AI Detection</h3>
              <p>Advanced ML algorithms detect anomalies and predict critical conditions</p>
            </div>

            <div className="home-feature-card">
              <div className="feature-icon-wrapper alert">
                <Zap size={24} />
              </div>
              <h3>Instant Alerts</h3>
              <p>Get immediate notifications for critical patient conditions</p>
            </div>

            <div className="home-feature-card">
              <div className="feature-icon-wrapper secure">
                <Shield size={24} />
              </div>
              <h3>Secure & Private</h3>
              <p>HIPAA compliant with end-to-end encryption for patient data</p>
            </div>

            <div className="home-feature-card">
              <div className="feature-icon-wrapper fog">
                <Activity size={24} />
              </div>
              <h3>Fog Computing</h3>
              <p>Edge processing for ultra-low latency and faster response times</p>
            </div>

            <div className="home-feature-card">
              <div className="feature-icon-wrapper team">
                <Users size={24} />
              </div>
              <h3>Multi-Patient</h3>
              <p>Monitor multiple patients simultaneously from a single dashboard</p>
            </div>
          </div>
        </main>
      </div>

      {/* Login Modal Overlay */}
      {showLogin && <Login />}
    </>
  )
}
