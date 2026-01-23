"""
Configuration Settings for SentimentScope
==========================================
Central configuration file for application settings, thresholds, and feature flags

PURPOSE:
    This module provides a centralized location for all configurable parameters
    used throughout the SentimentScope application. It loads settings from
    environment variables (via .env file) with sensible defaults.

CONFIGURATION CATEGORIES:
    1. App Configuration - Title, version, branding
    2. Model Settings - Sentiment classification thresholds
    3. UI Settings - Display preferences and history limits
    4. Analysis Settings - Text length limits and validation
    5. Color Scheme - Consistent color palette across app
    6. Export Settings - File format and timestamp configuration
    7. Feature Flags - Enable/disable experimental features

ENVIRONMENT VARIABLES:
    Settings can be customized by creating a .env file with:
    - APP_TITLE - Application name
    - APP_ICON - Emoji or icon for branding
    - POSITIVE_THRESHOLD - Min polarity for positive classification
    - NEGATIVE_THRESHOLD - Max polarity for negative classification
    - MAX_HISTORY_ITEMS - Number of analyses to keep in history
    - DEFAULT_THEME - UI theme preference

USAGE EXAMPLE:
    ```python
    from config import POSITIVE_THRESHOLD, COLORS
    
    if polarity >= POSITIVE_THRESHOLD:
        color = COLORS['positive']
    ```

BENEFITS:
    ✅ Single source of truth for all settings
    ✅ Easy to modify without changing code
    ✅ Environment-specific configurations
    ✅ Type-safe with explicit conversions
    ✅ Clear documentation of all options

Author: Ishan Chakraborty
Email: ishanrock1234@gmail.com
GitHub: @Ishan96Dev
License: MIT
Copyright (c) 2026
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
