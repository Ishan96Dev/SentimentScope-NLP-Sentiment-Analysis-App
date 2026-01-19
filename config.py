"""
Configuration settings for SentimentScope

Author: Ishan Chakraborty
License: MIT
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Configuration
APP_TITLE = os.getenv("APP_TITLE", "SentimentScope")
APP_ICON = os.getenv("APP_ICON", "🧠")
APP_VERSION = "1.0.0"

# Model Settings
POSITIVE_THRESHOLD = float(os.getenv("POSITIVE_THRESHOLD", "0.1"))
NEGATIVE_THRESHOLD = float(os.getenv("NEGATIVE_THRESHOLD", "-0.1"))

# UI Settings
MAX_HISTORY_ITEMS = int(os.getenv("MAX_HISTORY_ITEMS", "10"))
DEFAULT_THEME = os.getenv("DEFAULT_THEME", "light")

# Analysis Settings
MIN_TEXT_LENGTH = 5  # Minimum characters for analysis
MAX_TEXT_LENGTH = 5000  # Maximum characters for analysis
DEFAULT_CONFIDENCE_THRESHOLD = 55.0  # Minimum confidence for clear sentiment

# Color Scheme
COLORS = {
    "positive": "#10b981",  # Green
    "neutral": "#f59e0b",   # Orange/Yellow
    "negative": "#ef4444",  # Red
    "primary": "#667eea",   # Purple/Blue
    "secondary": "#764ba2"  # Purple
}

# Export Settings
EXPORT_FORMAT = "txt"
EXPORT_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# Feature Flags (for future features)
ENABLE_BATCH_ANALYSIS = False
ENABLE_MULTI_LANGUAGE = False
ENABLE_EMOTION_DETECTION = False
ENABLE_API = False
