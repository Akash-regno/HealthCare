# 🏥 Smart Healthcare Monitoring System

Real-time healthcare monitoring dashboard with ML-powered anomaly detection and email alerts.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18.0+-61dafb.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.0+-3178c6.svg)

## ✨ Features

- 🔐 **Authentication** - Login/Signup with protected routes
- 📊 **Real-time Monitoring** - Live patient vitals with auto-refresh
- 🧠 **ML Detection** - ECG-based RandomForest model (98.4% accuracy)
- 📧 **Email Alerts** - Automatic notifications for critical patients
- 🎨 **Modern UI** - Dark theme with smooth animations
- 📈 **Live Charts** - Real-time trend visualization

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Gmail account (for email alerts)

### Installation

**1. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**2. Install React dependencies**
```bash
cd frontend-react
npm install
cd ..
```

**3. Configure Email (Optional)**
- Open `email_notification.py`
- Update Gmail credentials (lines 17-23)
- See `EMAIL_QUICK_SETUP.md` for detailed steps

### Run the System

**Start all services:**
```bash
# Terminal 1 - Backend
cd cloud_server
python app.py

# Terminal 2 - Simulator
python ecg_simulator.py

# Terminal 3 - Frontend
cd frontend-react
npm run dev
```

**Access Dashboard:**
- Open: http://localhost:5173
- Click "Get Started" to create account
- Login and access dashboard

## 📁 Project Structure

```
├── cloud_server/
│   ├── app.py              # Flask REST API
│   ├── db.py               # Database setup
│   └── healthcare.db       # SQLite database
├── frontend-react/
│   ├── src/
│   │   ├── App.tsx         # Main app with routing
│   │   ├── pages/          # Home, Login, Dashboard, Patients, Alerts
│   │   └── components/     # VitalChart, LoadingSpinner, ErrorMessage
│   └── package.json
├── ecg_simulator.py        # Patient data simulator
├── ecg_model.pkl           # Trained ML model
├── email_notification.py   # Email alert service
└── requirements.txt
```

## 🔧 API Endpoints

- `GET /api/patients` - Get all patients
- `GET /api/patients/<id>/status` - Get patient status
- `GET /api/alerts` - Get all alerts
- `POST /api/health` - Update patient data
- `POST /api/alerts` - Create alert

## 🧠 ML Model

- **Algorithm**: RandomForest Classifier
- **Features**: ECG mean, std, min, max, median
- **Accuracy**: 98.4%
- **Dataset**: 200 ECG samples (147 normal, 53 abnormal)

## 📧 Email Notifications

When critical patients are detected, doctors receive professional HTML emails with:
- Patient ID and status
- All vital signs (HR, SpO2, Temperature, Acceleration)
- Timestamp
- Color-coded severity

**Setup:** See `EMAIL_QUICK_SETUP.md` for 5-minute Gmail configuration.

## 🎨 Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite
- React Router
- Recharts
- Lucide Icons

**Backend:**
- Flask + Flask-CORS
- SQLite
- Python 3.8+

**ML:**
- Scikit-learn
- Pandas
- NumPy
- Joblib

## 📊 Dashboard Pages

1. **Home** - Landing page with features
2. **Login** - Authentication modal
3. **Dashboard** - Live stats, charts, and alerts
4. **Patients** - Patient management and details
5. **Alerts** - Alert history with search/filter

## � Troubleshooting

**Backend not starting:**
```bash
# Check port 5000
netstat -ano | findstr :5000
```

**Frontend not loading:**
- Verify backend is running: http://127.0.0.1:5000/api/patients
- Hard refresh browser: Ctrl + Shift + R

**Email not working:**
- Check Gmail credentials in `email_notification.py`
- Enable 2-Step Verification
- Use App Password (not regular password)
- See `EMAIL_SETUP_GUIDE.txt`

## 📈 Performance

- Backend Response: <50ms
- ML Inference: <1ms
- Data Update: Every 2 seconds
- Chart Refresh: Every 3 seconds

## � Future Enhancements

- WebSocket for real-time updates
- Multi-patient support
- Historical data analysis
- Mobile app
- Docker deployment

## 📄 License

MIT License - See LICENSE file for details

---

**Built with ❤️ for Healthcare Innovation**

⭐ Star this repo if you find it helpful!
