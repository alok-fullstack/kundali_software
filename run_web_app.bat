@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo ============================================
echo    KUNDALI WEB APPLICATION
echo    Starting server...
echo ============================================
echo.
echo Browser mein ye URL kholo:
echo    http://localhost:5000
echo.
echo Server band karne ke liye Ctrl+C dabao
echo.
echo ============================================
echo.
start http://localhost:5000
python web_app.py
pause
