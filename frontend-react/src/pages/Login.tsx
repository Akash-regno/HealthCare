import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Activity, Mail, Lock, User, Eye, EyeOff, X } from 'lucide-react'

export default function Login() {
  const [isLogin, setIsLogin] = useState(true)
  const [showPassword, setShowPassword] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  })
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    // Basic validation
    if (!formData.email || !formData.password) {
      setError('Please fill in all fields')
      return
    }

    if (!isLogin && !formData.name) {
      setError('Please enter your name')
      return
    }

    // Simple authentication (in production, this would call an API)
    if (isLogin) {
      // For demo, accept any email/password
      localStorage.setItem('isAuthenticated', 'true')
      localStorage.setItem('userName', formData.email.split('@')[0])
      navigate('/dashboard')
    } else {
      // Sign up
      localStorage.setItem('isAuthenticated', 'true')
      localStorage.setItem('userName', formData.name)
      navigate('/dashboard')
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="auth-modal-overlay">
      <div className="auth-modal">
        <button className="modal-close" onClick={() => navigate('/')}>
          <X size={24} />
        </button>

        <div className="modal-icon">
          <Activity size={48} />
        </div>

        <h1 className="modal-title">
          {isLogin ? 'Welcome back' : 'Create account'}
        </h1>
        <p className="modal-subtitle">
          {isLogin ? 'Sign in to continue to HealthCare' : 'Sign up to get started with HealthCare'}
        </p>

        <form onSubmit={handleSubmit} className="modal-form">
          {!isLogin && (
            <div className="modal-field">
              <label>Name</label>
              <div className="modal-input">
                <User size={20} />
                <input
                  type="text"
                  name="name"
                  placeholder="Your full name"
                  value={formData.name}
                  onChange={handleChange}
                />
              </div>
            </div>
          )}

          <div className="modal-field">
            <label>Email</label>
            <div className="modal-input">
              <Mail size={20} />
              <input
                type="email"
                name="email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="modal-field">
            <label>Password</label>
            <div className="modal-input">
              <Lock size={20} />
              <input
                type={showPassword ? 'text' : 'password'}
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
              />
              <button
                type="button"
                className="password-eye"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>

          {error && <div className="modal-error">{error}</div>}

          <button type="submit" className="modal-submit">
            {isLogin ? 'Sign In' : 'Sign Up'}
          </button>
        </form>

        <div className="modal-footer">
          <span>{isLogin ? "Don't have an account?" : 'Already have an account?'}</span>
          <button onClick={() => setIsLogin(!isLogin)} className="modal-link">
            {isLogin ? 'Sign up' : 'Sign in'}
          </button>
        </div>
      </div>
    </div>
  )
}
