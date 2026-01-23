"""
Home Screen - Main Sentiment Analyzer Interface
================================================
Primary user interface for text input and sentiment analysis

PURPOSE:
    This is the main screen where users interact with the sentiment analyzer.
    Users can input text, trigger analysis, and view comprehensive results including
    overall sentiment, word-level impact analysis, and visual representations.

KEY FEATURES:
    ✅ Text input with character/word counter
    ✅ Quick example buttons for testing (Positive, Neutral, Negative)
    ✅ Real-time sentiment analysis with confidence scores
    ✅ Word-level sentiment impact identification
    ✅ Visual polarity gauge with interactive chart
    ✅ Highlighted text showing sentiment-bearing words
    ✅ Analysis history (last 10 analyses)
    ✅ Export functionality for results

SECURITY MEASURES:
    🛡️ Input validation - Length and content checks
    🛡️ Rate limiting - 10 requests/minute, 100/hour
    🛡️ Spam detection - Pattern-based filtering
    🛡️ Text sanitization - XSS and injection prevention
    🛡️ Security logging - All events tracked

LAYOUT STRUCTURE:
    ┌─────────────────────────────────────────────────────┐
    │ Header: Title and subtitle                          │
    ├──────────────────────┬──────────────────────────────┤
    │ Left Column (2/3)    │ Right Column (1/3)           │
    │ - Quick examples     │ - How It Works               │
    │ - Text input area    │ - Sentiment Types            │
    │ - Character counter  │                              │
    │ - Analyze button     │                              │
    │ - Results display    │                              │
    │   • Overall metrics  │                              │
    │   • Polarity gauge   │                              │
    │   • Word keywords    │                              │
    │   • Highlighted text │                              │
    └──────────────────────┴──────────────────────────────┘
    │ History Section (collapsible)                       │
    │ - Last 10 analyses with timestamps                  │
    └─────────────────────────────────────────────────────┘

USER WORKFLOW:
    1. User enters or pastes text (or clicks example button)
    2. System validates input (length, content, security)
    3. Rate limiter checks request allowance
    4. Text is sanitized and analyzed
    5. Results displayed with:
       - Overall sentiment (Positive/Neutral/Negative)
       - Confidence percentage and polarity score
       - Word-level keyword analysis
       - Visual gauge chart
       - Highlighted text with sentiment words
    6. Result added to history
    7. Export option available

TECHNICAL DETAILS:
    Data Structures: Dictionary (results), List (history, word sentiments)
    Algorithms: NLP analysis (O(n+m)), validation (O(n)), highlighting (O(n×m))
    State Management: Streamlit session state for history and examples
    Visualization: Plotly gauge charts, custom HTML/CSS for highlights

Author: Ishan Chakraborty
Email: ishanrock1234@gmail.com
GitHub: @Ishan96Dev
License: MIT
Copyright (c) 2026
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
                st.session_state.example_text = "I absolutely loved this experience! 🎉 It was amazing and exceeded all my expectations. 😍"
        
        with example_cols[1]:
            if st.button("😐 Neutral Example"):
                st.session_state.example_text = "The product arrived on time. 📦 It works as described. ✅"
        
        with example_cols[2]:
            if st.button("😠 Negative Example"):
                st.session_state.example_text = "This is the worst service I've ever experienced. 😤 Completely disappointed and frustrated. 😞"
        
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
                                # DSA COMPLEXITY: O(1) for insert at head, O(n) for slicing if >10
                                # Data Structure: List used as a Stack (LIFO) with size limit
                                # insert(0, item) is O(n) but n ≤ 10 (bounded), so O(1) in practice
                                st.session_state.history.insert(0, {
                                    "text": sanitized_text[:100] + "..." if len(sanitized_text) > 100 else sanitized_text,
                                    "result": result,
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                })
                                
                                # Keep only last 10 analyses
                                # DSA: List slicing O(k) where k=10, bounded constant time
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
                                
                                # =============================================
                                # EMOTION DETECTION (NEW FEATURE)
                                # =============================================
                                
                                emotions = result.get('emotions', {})
                                if emotions and emotions.get('emotion_detected'):
                                    st.markdown("#### 🎭 Emotion Detection")
                                    
                                    emotion_col1, emotion_col2 = st.columns([1, 2])
                                    
                                    with emotion_col1:
                                        # Primary emotion display
                                        primary_emotion = emotions['primary_emotion']
                                        confidence = emotions['confidence']
                                        
                                        emotion_icons = {
                                            "Joy": "😊",
                                            "Sadness": "😢",
                                            "Anger": "😡",
                                            "Fear": "😰",
                                            "Surprise": "😲",
                                            "Disgust": "🤢",
                                            "Trust": "🤝",
                                            "Anticipation": "🤔"
                                        }
                                        
                                        icon = emotion_icons.get(primary_emotion, "😐")
                                        
                                        st.markdown(f"""
                                        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                                    padding: 20px; border-radius: 12px; text-align: center; color: white;'>
                                            <div style='font-size: 48px; margin-bottom: 10px;'>{icon}</div>
                                            <div style='font-size: 24px; font-weight: bold;'>{primary_emotion}</div>
                                            <div style='font-size: 16px; opacity: 0.9;'>{confidence:.1f}% confidence</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    with emotion_col2:
                                        # Top 3 emotions radar chart
                                        st.markdown("**Emotion Breakdown:**")
                                        
                                        top_emotions = emotions.get('top_emotions', [])
                                        for emo in top_emotions:
                                            emotion_name = emo['emotion'].capitalize()
                                            score = emo['score']
                                            icon = emotion_icons.get(emotion_name, "😐")
                                            
                                            st.markdown(f"{icon} **{emotion_name}**: {score:.1f}%")
                                            st.progress(score / 100)
                                
                                # =============================================
                                # ADVANCED KEYWORD EXTRACTION (NEW FEATURE)
                                # =============================================
                                
                                advanced_keywords = result.get('advanced_keywords', {})
                                if advanced_keywords:
                                    st.markdown("#### 🔑 Advanced Keyword Analysis")
                                    
                                    kw_col1, kw_col2 = st.columns(2)
                                    
                                    with kw_col1:
                                        noun_phrases = advanced_keywords.get('noun_phrases', [])
                                        if noun_phrases:
                                            st.markdown("**📝 Key Phrases:**")
                                            for phrase in noun_phrases:
                                                st.markdown(f"• `{phrase}`")
                                    
                                    with kw_col2:
                                        frequent_words = advanced_keywords.get('frequent_words', [])[:5]
                                        if frequent_words:
                                            st.markdown("**🔤 Most Frequent:**")
                                            for word in frequent_words:
                                                st.markdown(f"• `{word}`")
                                
                                # =============================================
                                # WORD-LEVEL SENTIMENT ANALYSIS
                                # =============================================
                                
                                st.markdown("#### 🔤 Word-Level Sentiment Impact")
                                st.markdown("See which words are driving the overall sentiment:")
                                
                                # Get word sentiments and keywords
                                word_sentiments = result.get('word_sentiments', [])
                                sentiment_keywords = result.get('sentiment_keywords', {})
                                
                                if word_sentiments:
                                    # Display top impactful words
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        st.markdown("##### 😊 Positive Keywords")
                                        positive_words = sentiment_keywords.get('positive', [])
                                        
                                        if positive_words:
                                            for word_data in positive_words:
                                                word = word_data['word']
                                                polarity = word_data['polarity']
                                                impact = word_data['impact']
                                                
                                                st.markdown(f"""
                                                <div style='background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                                                            padding: 10px; border-radius: 8px; margin: 5px 0;'>
                                                    <b style='color: #065f46;'>"{word}"</b><br>
                                                    <small>Polarity: +{polarity:.3f} | Impact: {impact:.3f}</small>
                                                </div>
                                                """, unsafe_allow_html=True)
                                        else:
                                            st.info("No strong positive words detected")
                                    
                                    with col2:
                                        st.markdown("##### 😠 Negative Keywords")
                                        negative_words = sentiment_keywords.get('negative', [])
                                        
                                        if negative_words:
                                            for word_data in negative_words:
                                                word = word_data['word']
                                                polarity = word_data['polarity']
                                                impact = word_data['impact']
                                                
                                                st.markdown(f"""
                                                <div style='background: linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%); 
                                                            padding: 10px; border-radius: 8px; margin: 5px 0;'>
                                                    <b style='color: #991b1b;'>"{word}"</b><br>
                                                    <small>Polarity: {polarity:.3f} | Impact: {impact:.3f}</small>
                                                </div>
                                                """, unsafe_allow_html=True)
                                        else:
                                            st.info("No strong negative words detected")
                                    
                                    # Summary statistics
                                    st.markdown("##### 📊 Word Sentiment Summary")
                                    
                                    col1, col2, col3 = st.columns(3)
                                    
                                    with col1:
                                        total_positive = sentiment_keywords.get('total_positive', 0)
                                        st.metric("Positive Words", total_positive)
                                    
                                    with col2:
                                        total_negative = sentiment_keywords.get('total_negative', 0)
                                        st.metric("Negative Words", total_negative)
                                    
                                    with col3:
                                        ratio = total_positive / max(total_negative, 1) if total_negative > 0 else total_positive
                                        st.metric("Pos/Neg Ratio", f"{ratio:.2f}")
                                    
                                    # Highlighted text with sentiment words
                                    with st.expander("📝 View Text with Sentiment Highlights", expanded=False):
                                        st.markdown("**Original text with sentiment-bearing words highlighted:**")
                                        
                                        # Create highlighted version
                                        highlighted_text = sanitized_text
                                        
                                        # Sort by word length (descending) to avoid partial replacements
                                        sorted_words = sorted(word_sentiments, key=lambda x: len(x['word']), reverse=True)
                                        
                                        for word_data in sorted_words:
                                            word = word_data['word']
                                            sentiment = word_data['sentiment']
                                            polarity = word_data['polarity']
                                            
                                            # Choose color based on sentiment
                                            if sentiment == "Positive":
                                                color = "#d1fae5"
                                                text_color = "#065f46"
                                            elif sentiment == "Negative":
                                                color = "#fee2e2"
                                                text_color = "#991b1b"
                                            else:
                                                color = "#fef3c7"
                                                text_color = "#92400e"
                                            
                                            # Replace word with highlighted version (case-insensitive)
                                            import re
                                            pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
                                            highlighted_text = pattern.sub(
                                                f'<span style="background-color: {color}; color: {text_color}; '
                                                f'padding: 2px 4px; border-radius: 3px; font-weight: bold;" '
                                                f'title="Polarity: {polarity:.3f}">{word}</span>',
                                                highlighted_text,
                                                count=1  # Highlight first occurrence only
                                            )
                                        
                                        st.markdown(f'<div style="line-height: 1.8; font-size: 16px;">{highlighted_text}</div>', 
                                                   unsafe_allow_html=True)
                                        
                                        st.caption("💡 Hover over highlighted words to see their polarity scores")
                                
                                else:
                                    st.info("ℹ️ No significant sentiment-bearing words detected in this text.")
                                
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
