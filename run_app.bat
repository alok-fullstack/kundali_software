@echo off
echo ============================================================
echo   KUNDALI SOFTWARE - Next.js + FastAPI
echo   With Auto-Reload enabled for both servers
echo ============================================================
echo.

REM Kill any existing processes on the ports
echo Cleaning up old processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do taskkill /F /PID %%a 2>nul
timeout /t 2 >nul

echo.
echo Starting FastAPI Backend (Port 8000) with auto-reload...
start "FastAPI Backend" cmd /k "cd /d %~dp0backend && python -c "import sys; sys.path.insert(0,'..'); import uvicorn; uvicorn.run('app:app', host='127.0.0.1', port=8000, reload=True)""

echo Starting Next.js Frontend (Port 3000) with hot-reload...
start "Next.js Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ============================================================
echo   SERVERS STARTED WITH AUTO-RELOAD
echo ============================================================
echo.
echo   Backend API:  http://localhost:8000
echo   API Docs:     http://localhost:8000/docs
echo   Frontend:     http://localhost:3000
echo.
echo   Auto-reload is ENABLED:
echo   - FastAPI: Edit Python files, server reloads automatically
echo   - Next.js: Edit React files, page updates automatically
echo.
echo   To stop: Close the terminal windows or press Ctrl+C in each
echo ============================================================
echo.
pause
