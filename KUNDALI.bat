@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo  =============================================
echo       VISTRUT KUNDALI SOFTWARE
echo       (Detailed Kundali Generator)
echo  =============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed!
    pause
    exit /b
)

:: Install dependencies
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install flask pyswisseph pytz geopy pydantic --quiet
)

:: Open browser after 2 seconds
start /b cmd /c "timeout /t 2 >nul && start http://localhost:5000"

echo.
echo  Browser mein khulega: http://localhost:5000
echo.
echo  Band karne ke liye ye window close karo
echo.
echo  =============================================
echo.

python kundali_web.py
