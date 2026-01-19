#!/bin/bash

echo "========================================"
echo "SentimentScope - Setup & Installation"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed!"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "Python found:"
python3 --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created successfully!"
else
    echo "Virtual environment already exists."
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo ""

# Download NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('brown'); nltk.download('punkt'); nltk.download('punkt_tab')"
echo ""

echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "To run the app, use: ./run.sh"
echo "Or manually run: streamlit run app.py"
echo ""
