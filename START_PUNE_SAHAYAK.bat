@echo off
setlocal
cd /d "%~dp0"
echo ============================================
echo        PuneSahayak - Your daily commute
echo ============================================
if not exist ".venv\Scripts\python.exe" (
    echo Creating Python virtual environment...
    py -3 -m venv .venv
    if errorlevel 1 (
        echo Could not create the environment. Install Python 3.10+ and try again.
        pause
        exit /b 1
    )
)
echo Installing / checking required packages...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Package installation failed. Check your internet connection.
    pause
    exit /b 1
)
echo Starting PuneSahayak...
".venv\Scripts\python.exe" -m streamlit run app.py
pause
