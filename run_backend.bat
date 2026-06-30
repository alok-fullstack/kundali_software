@echo off
echo ============================================================
echo    KUNDALI SOFTWARE - FastAPI Backend
echo ============================================================
echo.
echo Starting server at http://localhost:8000
echo API documentation at http://localhost:8000/docs
echo.

cd /d "%~dp0backend"
python run.py

pause
