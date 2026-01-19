"""
SentimentScope - NLP-based Sentiment Detection App
====================================================
Main entry point with navigation and security initialization

This module serves as the primary entry point for the SentimentScope application.
It handles:
- Page configuration and layout setup
- Security session initialization
- Navigation between different screens (Home and About)
- Sidebar menu with statistics and rate limit display
- Custom CSS styling for professional UI

Author: Ishan Chakraborty
Email: ishanrock1234@gmail.com
GitHub: @Ishan96Dev
License: MIT
Copyright (c) 2026
"""

# ============================================================================
# IMPORTS - Standard and Third-Party Libraries
# ============================================================================

import streamlit as st  # Main web application framework
from streamlit_option_menu import option_menu  # Custom navigation menu component

# ============================================================================
# IMPORTS - Application Modules
# ============================================================================

# Import UI screens - each screen is a separate module for better organization
from ui import home, about  # home: Main sentiment analyzer, about: App information

# Import security utilities - handle validation, rate limiting, and logging
from utils.security import SessionManager, SecurityLogger

# ============================================================================
# SECURITY INITIALIZATION
# ============================================================================

# Initialize security session before any user interaction
# This sets up session state variables for tracking and security
SessionManager.initialize_session()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

# Configure Streamlit page settings before any other st commands
# This must be the first Streamlit command in the script
st.set_page_config(
    page_title="SentimentScope - Sentiment Analysis",  # Browser tab title
    page_icon="🧠",  # Browser tab icon (brain emoji represents NLP/AI)
    layout="wide",  # Use full width of browser window for better UX
    initial_sidebar_state="expanded"  # Show sidebar by default for easy navigation
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

# Inject custom CSS for professional and polished UI appearance
# Using markdown with unsafe_allow_html=True to embed CSS styles
st.markdown("""
    <style>
    /* Main content area padding for better spacing */
    .main {
        padding: 2rem;  /* 2rem = 32px padding on all sides */
    }
    
    /* Style all buttons consistently across the app */
    .stButton>button {
        width: 100%;  /* Full width buttons for better mobile UX */
        border-radius: 8px;  /* Rounded corners for modern look */
        height: 3em;  /* Fixed height for consistent button sizing */
        font-weight: 600;  /* Semi-bold text for better readability */
    }
    
    /* Sentiment result card container styles */
    .sentiment-card {
        padding: 2rem;  /* Internal spacing */
        border-radius: 10px;  /* Rounded corners */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  /* Subtle shadow for depth */
        margin: 1rem 0;  /* Vertical spacing between cards */
    }
    
    /* Positive sentiment styling - purple gradient background */
    .positive {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;  /* White text for contrast on dark background */
    }
    
    /* Negative sentiment styling - pink/red gradient background */
    .negative {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;  /* White text for contrast */
    }
    
    /* Neutral sentiment styling - blue/cyan gradient background */
    .neutral {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;  /* White text for contrast */
    }
    </style>
    """, unsafe_allow_html=True)  # Allow HTML/CSS injection (safe as it's our own code)

# ============================================================================
# SIDEBAR NAVIGATION AND STATS
# ============================================================================

# Create sidebar context - all code within this block appears in the sidebar
with st.sidebar:
    # --- App Branding ---
    st.markdown("### 🧠 SentimentScope")  # App name with brain emoji
    st.markdown("*Powered by NLP*")  # Tagline in italics
    st.markdown("*by Ishan Chakraborty*")  # Author attribution
    st.markdown("---")  # Horizontal divider for visual separation
    
    # --- Navigation Menu ---
    # Create interactive menu using streamlit-option-menu library
    # Returns the selected option as a string
    selected = option_menu(
        menu_title=None,  # No title above menu (we have branding above)
        options=["Sentiment Analyzer", "About App"],  # Two main screens
        icons=["brain", "info-circle"],  # Bootstrap icons for each option
        menu_icon="cast",  # Icon for the menu itself (not used when menu_title is None)
        default_index=0,  # Start on first option (Sentiment Analyzer)
        styles={  # Custom CSS styling for the menu
            "container": {"padding": "0!important"},  # Remove default padding
            "icon": {"color": "#ffffff", "font-size": "20px"},  # White icons for visibility
            "nav-link": {  # Style for each menu option
                "font-size": "16px",  # Text size
                "text-align": "left",  # Left-aligned text
                "margin": "0px",  # No margin
                "--hover-color": "#f0f2f6",  # Light gray on hover
            },
            "nav-link-selected": {"background-color": "#667eea", "color": "#ffffff"},  # Purple background, white text for selected
        }
    )
    
    st.markdown("---")  # Divider between menu and stats
    
    # --- Usage Statistics ---
    st.markdown("##### 📊 Quick Stats")  # Stats section header
    
    # Initialize analysis counter in session state if not exists
    # Session state persists data across reruns of the script
    if "analysis_count" not in st.session_state:
        st.session_state.analysis_count = 0  # Start at zero
    
    # Display total analyses performed this session as a metric card
    st.metric("Analyses Performed", st.session_state.analysis_count)
    
    # --- Rate Limit Display ---
    from utils.security import RateLimiter  # Import rate limiter (lazy import)
    
    # Get current usage statistics (requests made and remaining)
    usage_stats = RateLimiter.get_usage_stats()
    
    st.markdown("##### 🛡️ Rate Limits")  # Rate limit section header
    
    # Display remaining requests per minute
    st.caption(f"Remaining this minute: {usage_stats['remaining_minute']}/{RateLimiter.MAX_REQUESTS_PER_MINUTE}")
    
    # Display remaining requests per hour
    st.caption(f"Remaining this hour: {usage_stats['remaining_hour']}/{RateLimiter.MAX_REQUESTS_PER_HOUR}")

# ============================================================================
# SCREEN ROUTING
# ============================================================================

# Route to appropriate screen based on sidebar menu selection
# The 'selected' variable contains the user's menu choice
if selected == "Sentiment Analyzer":
    # Display main sentiment analysis interface
    # Defined in ui/home.py
    home.render()
elif selected == "About App":
    # Display application information and documentation
    # Defined in ui/about.py
    about.render()

# ============================================================================
# SIDEBAR FOOTER
# ============================================================================

# Add footer to bottom of sidebar with app information
st.sidebar.markdown("---")  # Divider above footer

# Display footer with centered text, custom styling, and attribution
# Using HTML entity for heart to avoid encoding issues
st.sidebar.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
    Built with &hearts; using Streamlit<br>
    by <strong>Ishan Chakraborty</strong><br>
    &copy; 2026 SentimentScope | MIT License
    </div>
    """, 
    unsafe_allow_html=True  # Allow HTML for custom styling
)
