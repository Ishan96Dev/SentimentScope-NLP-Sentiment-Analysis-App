#!/bin/bash

echo "========================================"
echo "Starting SentimentScope Application"
echo "========================================"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found!"
fi
echo ""

# Run Streamlit app
echo "Starting Streamlit app..."
streamlit run app.py
