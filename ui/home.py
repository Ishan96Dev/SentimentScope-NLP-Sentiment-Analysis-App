"""
Home Screen - Main Sentiment Analyzer Interface
================================================
Primary user interface for text input and sentiment analysis

This module provides the main interactive interface where users:
- Enter or paste text for analysis
- Select quick example texts
- View character and word counts
- Trigger sentiment analysis
- See comprehensive results with visualizations
- Access analysis history
- Export results to file

The interface implements comprehensive security measures:
- Input validation before analysis
- Rate limiting to prevent abuse
- Spam detection and blocking
- Text sanitization for safety
- Error handling for robustness

Layout Structure:
┌─────────────────────────────────────────┐
│ Header: Title and subtitle             │
├──────────────────┬──────────────────────┤
│ Left Column      │ Right Column         │
│ - Quick examples │ - Instructions       │
│ - Text input     │ - Sentiment types    │
│ - Char counter   │                      │
│ - Analyze button │                      │
│ - Results        │                      │
└──────────────────┴──────────────────────┘
│ History Section (collapsible)          │
└─────────────────────────────────────────┘

Author: Ishan Chakraborty
Email: ishanrock1234@gmail.com
GitHub: @Ishan96Dev
License: MIT
"""

# ============================================================================
# IMPORTS
# ============================================================================

import streamlit as st  # Main web framework
import plotly.graph_objects as go  # Interactive visualizations (gauge chart)
from sentiment.analyzer import get_analyzer  # Sentiment analysis engine
from datetime import datetime  # Timestamp generation for history
from utils.security import InputValidator, RateLimiter, SecurityLogger  # Security utilities


# ============================================================================
# MAIN RENDER FUNCTION
# ============================================================================

def render():
    """
    Render the main sentiment analyzer screen
    
    This function creates the complete user interface including:
    - Header section with title and subtitle
    - Two-column layout (input + info)
    - Quick example buttons for testing
    - Text input area with character counter
    - Analysis button with security checks
    - Comprehensive results display
    - Interactive visualizations
    - Analysis history panel
    
    The function manages session state for:
    - Example text selection
    - Analysis history (last 10)
    - Analysis counter
    
    Security Flow:
    1. Validate input (length, content, format)
    2. Check rate limit (10/min, 100/hour)
    3. Sanitize text (remove dangerous content)
    4. Check for spam (pattern detection)
    5. Analyze sentiment (if all checks pass)
    6. Display results or error messages
    """
    
    # =========================================================================
    # HEADER SECTION - Title and subtitle
    # =========================================================================
    
    st.markdown("# 🧠 Sentiment Analyzer")  # Main title with brain emoji
    st.markdown("### Analyze text sentiment with AI-powered NLP")  # Subtitle
    st.markdown("---")  # Horizontal divider for visual separation
    
    # =========================================================================
    # SESSION STATE INITIALIZATION - Set up history tracking
    # =========================================================================
    
    # Initialize history list in session state if it doesn't exist
    # Session state persists across Streamlit reruns
    # History stores the last 10 sentiment analyses
    if "history" not in st.session_state:
        st.session_state.history = []  # Empty list to start
    
    # Main layout - two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input section
        st.markdown("#### 📝 Enter Your Text")
        
        # Example buttons
        st.markdown("**Quick Examples:**")
        example_cols = st.columns(3)
        
        with example_cols[0]:
            if st.button("😊 Positive Example"):
                st.session_state.example_text = "I absolutely loved this experience! 🎉 It was amazing and exceeded all my expectations. The team was fantastic! 👏✨"
        
        with example_cols[1]:
            if st.button("😐 Neutral Example"):
                st.session_state.example_text = "The product arrived on time 📦. It works as described. Standard service, nothing exceptional."
        
        with example_cols[2]:
            if st.button("😠 Negative Example"):
                st.session_state.example_text = "This is the worst service I've ever experienced 😤. Completely disappointed and frustrated. Never again! 👎"
        
        # Text area
        default_text = st.session_state.get("example_text", "")
        text_input = st.text_area(
            label="Text to analyze",
            value=default_text,
            height=200,
            placeholder="Enter your text here...\n\nExample: I absolutely loved the experience! The service was outstanding.",
            help="Enter any text to analyze its sentiment",
            label_visibility="collapsed"
        )
        
        # Character counter
        if text_input:
            char_count = len(text_input)
            word_count = len(text_input.split())
            st.caption(f"📊 {char_count} characters • {word_count} words")
        
        # Action buttons
        button_cols = st.columns([1, 1, 2])
        
        with button_cols[0]:
            analyze_button = st.button("🔍 Analyze Sentiment", type="primary")
        
        with button_cols[1]:
            clear_button = st.button("🗑️ Clear")
        
        # Clear functionality
        if clear_button:
            st.session_state.example_text = ""
            st.rerun()
    
    with col2:
        # Info panel
        st.markdown("#### ℹ️ How It Works")
        st.info("""
        1. **Enter** or paste your text
        2. Click **Analyze** button
        3. View sentiment results with confidence score
        4. See visual breakdown
        """)
        
        st.markdown("#### 🎯 Sentiment Types")
        st.markdown("""
        - 😊 **Positive**: Happy, satisfied, pleased
        - 😐 **Neutral**: Factual, objective, balanced
        - 😠 **Negative**: Sad, angry, dissatisfied
        """)
    
    # Analysis section
    if analyze_button:
        if not text_input or not text_input.strip():
            st.error("⚠️ Please enter some text to analyze!")
        else:
            # Security: Validate input
            is_valid, error_message = InputValidator.validate_input(text_input)
            if not is_valid:
                st.error(error_message)
                SecurityLogger.log_event("validation_error", error_message)
            else:
                # Security: Check rate limit
                is_allowed, rate_limit_message = RateLimiter.check_rate_limit()
                if not is_allowed:
                    st.warning(rate_limit_message)
                    SecurityLogger.log_event("rate_limit", rate_limit_message)
                else:
                    # Security: Sanitize input
                    sanitized_text = InputValidator.sanitize_text(text_input)
                    
                    # Security: Check for spam
                    if InputValidator.is_spam(sanitized_text):
                        st.error("⚠️ Spam content detected. Please enter legitimate text.")
                        SecurityLogger.log_event("spam_detected", "Spam content blocked")
                    else:
                        with st.spinner("🔄 Analyzing sentiment..."):
                            try:
                                # Get analyzer and perform analysis
                                analyzer = get_analyzer()
                                result = analyzer.analyze(sanitized_text)
                                
                                # Increment counter
                                st.session_state.analysis_count = st.session_state.get("analysis_count", 0) + 1
                                
                                # Add to history
                                st.session_state.history.insert(0, {
                                    "text": sanitized_text[:100] + "..." if len(sanitized_text) > 100 else sanitized_text,
                                    "result": result,
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                })
                                
                                # Keep only last 10 analyses
                                if len(st.session_state.history) > 10:
                                    st.session_state.history = st.session_state.history[:10]
                                
                                # Log successful analysis
                                SecurityLogger.log_event("analysis_success", f"Analyzed {len(sanitized_text)} characters")
                    
                                # Display results
                                st.markdown("---")
                                st.markdown("## 📊 Analysis Results")
                                
                                # Main result card
                                result_col1, result_col2, result_col3 = st.columns([1, 2, 1])
                                
                                with result_col1:
                                    st.markdown(f"<h1 style='text-align: center; font-size: 5em;'>{result['emoji']}</h1>", unsafe_allow_html=True)
                                
                                with result_col2:
                                    st.markdown(f"### Sentiment: **{result['label']}**")
                                    st.markdown(f"**Confidence:** {result['confidence']}%")
                                    
                                    # Confidence bar
                                    st.progress(result['confidence'] / 100)
                                    
                                with result_col3:
                                    st.metric(label="Polarity", value=result['polarity'], delta=None)
                                    st.metric(label="Subjectivity", value=result['subjectivity'], delta=None)
                                
                                # Detailed metrics
                                st.markdown("#### 📈 Detailed Analysis")
                                
                                metric_cols = st.columns(4)
                                
                                with metric_cols[0]:
                                    st.metric("Sentiment", result['label'], delta=None)
                                
                                with metric_cols[1]:
                                    st.metric("Confidence", f"{result['confidence']}%", delta=None)
                                
                                with metric_cols[2]:
                                    st.metric("Characters", result['text_length'], delta=None)
                                
                                with metric_cols[3]:
                                    st.metric("Words", result['word_count'], delta=None)
                                
                                # Visual gauge chart
                                st.markdown("#### 🎯 Sentiment Polarity Gauge")
                                
                                fig = go.Figure(go.Indicator(
                                    mode="gauge+number+delta",
                                    value=result['polarity'],
                                    domain={'x': [0, 1], 'y': [0, 1]},
                                    title={'text': "Polarity Score", 'font': {'size': 24}},
                                    delta={'reference': 0, 'increasing': {'color': "#10b981"}, 'decreasing': {'color': "#ef4444"}},
                                    gauge={
                                        'axis': {'range': [-1, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
                                        'bar': {'color': result['color']},
                                        'bgcolor': "white",
                                        'borderwidth': 2,
                                        'bordercolor': "gray",
                                        'steps': [
                                            {'range': [-1, -0.1], 'color': '#fee2e2'},
                                            {'range': [-0.1, 0.1], 'color': '#fef3c7'},
                                            {'range': [0.1, 1], 'color': '#d1fae5'}
                                        ],
                                        'threshold': {
                                            'line': {'color': "red", 'width': 4},
                                            'thickness': 0.75,
                                            'value': result['polarity']
                                        }
                                    }
                                ))
                                
                                fig.update_layout(
                                    height=300,
                                    margin=dict(l=20, r=20, t=40, b=20),
                                    paper_bgcolor="rgba(0,0,0,0)",
                                    font={'color': "#333", 'family': "Arial"}
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                                
                                # Interpretation
                                st.markdown("#### 💡 Interpretation")
                                
                                if result['label'] == "Positive":
                                    st.success(f"""
                                    ✅ The text expresses **positive sentiment** with {result['confidence']:.1f}% confidence.
                                    The overall tone is optimistic, happy, or satisfied.
                                    """)
                                elif result['label'] == "Negative":
                                    st.error(f"""
                                    ❌ The text expresses **negative sentiment** with {result['confidence']:.1f}% confidence.
                                    The overall tone is pessimistic, unhappy, or dissatisfied.
                                    """)
                                else:
                                    st.warning(f"""
                                    ➖ The text has **neutral sentiment** with {result['confidence']:.1f}% confidence.
                                    The tone is balanced, factual, or objective.
                                    """)
                                
                                # Export option
                                st.markdown("#### 💾 Export Results")
                                export_data = f"""
Sentiment Analysis Report
========================
Text: {sanitized_text[:200]}{"..." if len(sanitized_text) > 200 else ""}
Sentiment: {result['label']}
Confidence: {result['confidence']}%
Polarity: {result['polarity']}
Subjectivity: {result['subjectivity']}
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                                """
                                st.download_button(
                                    label="📥 Download Report",
                                    data=export_data,
                                    file_name=f"sentiment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                    mime="text/plain"
                                )
                            
                            except ValueError as e:
                                st.error(f"❌ Error: {str(e)}")
                                SecurityLogger.log_event("validation_error", str(e))
                            except Exception as e:
                                st.error(f"❌ An unexpected error occurred: {str(e)}")
                                SecurityLogger.log_event("analysis_error", str(e))
    
    # History section
    if st.session_state.history:
        st.markdown("---")
        st.markdown("## 📜 Recent Analyses")
        
        with st.expander("View Analysis History", expanded=False):
            for idx, item in enumerate(st.session_state.history[:5]):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
                
                with col1:
                    st.text(f"{item['text']}")
                
                with col2:
                    st.markdown(f"**{item['result']['label']}** {item['result']['emoji']}")
                
                with col3:
                    st.text(f"{item['result']['confidence']}%")
                
                with col4:
                    st.caption(item['timestamp'])
                
                if idx < len(st.session_state.history) - 1:
                    st.divider()
            
            if st.button("🗑️ Clear History"):
                st.session_state.history = []
                st.rerun()
