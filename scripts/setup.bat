@echo off
echo ========================================
echo SentimentScope - Setup & Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo.

REM Download NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('brown'); nltk.download('punkt'); nltk.download('punkt_tab')"
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the app, use: run.bat
echo Or manually run: streamlit run app.py
echo.
pause
