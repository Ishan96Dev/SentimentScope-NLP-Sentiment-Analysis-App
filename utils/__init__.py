"""
User Interface Module
=====================
Streamlit-based UI components for SentimentScope

PURPOSE:
    This package contains all user interface screens and components
    for the SentimentScope application. Each module represents a
    complete screen/page in the application.

SCREENS:
    1. home.py - Main sentiment analyzer interface
       - Text input and analysis
       - Results display with word-level insights
       - Analysis history
       
    2. analytics.py - Insights dashboard
       - Aggregate statistics
       - Word impact visualizations
       - Keyword frequency analysis
       
    3. about.py - Application information
       - What is sentiment analysis
       - How to use the app
       - Technology stack details

NAVIGATION:
    Screens are routed through app.py using streamlit-option-menu
    Each screen has a render() function called by the router

DESIGN PRINCIPLES:
    ✅ Responsive layouts with columns
    ✅ Consistent color scheme
    ✅ Interactive visualizations
    ✅ Clear information hierarchy
    ✅ Mobile-friendly design

Author: Ishan Chakraborty
License: MIT
"""

from ui import home, about, analytics

__all__ = ['home', 'about', 'analytics']
