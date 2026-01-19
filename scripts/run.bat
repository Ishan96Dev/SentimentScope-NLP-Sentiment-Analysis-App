@echo off
echo ========================================
echo Starting SentimentScope Application
echo ========================================
echo.
cd /d "%~dp0"
echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found!
)
echo.
echo Starting Streamlit app...
streamlit run app.py
pause
