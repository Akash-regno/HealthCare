@echo off
echo ========================================
echo Smart Healthcare Monitoring System
echo ========================================
echo.

echo Starting Flask Backend...
start "Flask Backend" cmd /k "cd cloud_server && python app.py"
timeout /t 2 /nobreak >nul

echo Starting Patient Simulator...
start "Patient Simulator" cmd /k "python direct_simulator.py"
timeout /t 2 /nobreak >nul

echo Starting React Frontend...
start "React Frontend" cmd /k "cd frontend-react && npm run dev"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo All services started!
echo ========================================
echo.
echo Backend:  http://127.0.0.1:5000
echo Frontend: http://localhost:5173
echo.
echo Press any key to open the dashboard...
pause >nul

start http://localhost:5173

echo.
echo To stop all services, close the terminal windows.
echo.
pause
