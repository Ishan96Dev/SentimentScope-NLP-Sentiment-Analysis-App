"""
About Screen - Application Information & Sentiment Analysis Guide
==================================================================
Informational interface providing details about SentimentScope and sentiment analysis

PURPOSE:
    This module serves as the information hub for the application, explaining:
    - What sentiment analysis is and how it works
    - Key features and capabilities of SentimentScope
    - How to use the application effectively
    - Technical implementation details
    - Security and privacy information

CONTENT SECTIONS:
    1. Introduction - What is SentimentScope
    2. What is Sentiment Analysis - Educational content
    3. How It Works - Technical explanation
    4. Key Features - Application capabilities
    5. Sentiment Types - Classification categories
    6. Technology Stack - Libraries and frameworks used
    7. Use Cases - Real-world applications
    8. Getting Started - Quick start guide
    9. Security & Privacy - Data protection information

USER BENEFITS:
    - Learn about sentiment analysis concepts
    - Understand how to interpret results
    - Discover best practices for text analysis
    - Get started quickly with clear instructions

TECHNICAL DETAILS:
    Pure informational content, no data processing
    Uses Streamlit markdown and UI components
    Organized with expandable sections for better UX

Author: Ishan Chakraborty
Email: ishanrock1234@gmail.com
GitHub: @Ishan96Dev
License: MIT
Copyright (c) 2026
"""

import streamlit as st


def render():
    """
    Render the About screen for SentimentScope using Streamlit.
    
    Displays informational sections including an introduction, what sentiment analysis is, how the app works, technical details, example analyses, use cases, key features (current and planned), technology stack, security & privacy notes, limitations, a FAQ, and a feedback/footer area. This function directly renders UI components and does not return a value.
    """
    
    # Header
    st.markdown("# ℹ️ About SentimentScope")
    st.markdown("### Your AI-Powered Sentiment Analysis Companion")
    st.markdown("---")
    
    # Introduction
    st.markdown("""
    **SentimentScope** is a professional Natural Language Processing (NLP) application 
    that analyzes text sentiment in real-time. Whether you're analyzing customer feedback, 
    social media posts, or any text content, SentimentScope provides accurate and 
    insightful sentiment detection.
    """)
    
    st.markdown("")
    
    # What is Sentiment Analysis
    st.markdown("## 🎯 What is Sentiment Analysis?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Sentiment Analysis** (also called opinion mining) is the process of determining 
        the emotional tone behind a piece of text. It's a key task in Natural Language 
        Processing (NLP) that helps understand opinions, attitudes, and emotions expressed 
        in written language.
        
        ### Key Applications:
        - 📊 **Customer Feedback Analysis** - Understand customer satisfaction
        - 🐦 **Social Media Monitoring** - Track brand sentiment
        - 📧 **Email Classification** - Prioritize urgent communications
        - 💬 **Product Reviews** - Aggregate user opinions
        - 🎭 **Content Moderation** - Detect negative or toxic content
        """)
    
    with col2:
        st.info("""
        **💡 Did You Know?**
        
        Sentiment analysis is used by major companies like Amazon, Netflix, and Twitter 
        to understand customer opinions and improve their services.
        """)
    
    st.markdown("---")
    
    # How It Works
    st.markdown("## ⚙️ How SentimentScope Works")
    
    st.markdown("""
    SentimentScope uses a multi-step process to analyze sentiment:
    """)
    
    step_cols = st.columns(4)
    
    with step_cols[0]:
        st.markdown("""
        ### 1️⃣ Input
        You provide the text you want to analyze
        """)
    
    with step_cols[1]:
        st.markdown("""
        ### 2️⃣ Processing
        The text is cleaned and preprocessed
        """)
    
    with step_cols[2]:
        st.markdown("""
        ### 3️⃣ Analysis
        NLP model evaluates sentiment
        """)
    
    with step_cols[3]:
        st.markdown("""
        ### 4️⃣ Results
        You get labeled sentiment with confidence
        """)
    
    st.markdown("")
    
    # Technical Details
    with st.expander("🔬 Technical Details", expanded=True):
        st.markdown("""
        ### NLP Model: TextBlob
        
        SentimentScope uses **TextBlob**, a powerful Python library for processing textual data.
        TextBlob provides a simple API for common NLP tasks including sentiment analysis.
        
        **Key Features:**
        - **Polarity Score**: Ranges from -1 (most negative) to +1 (most positive)
        - **Subjectivity Score**: Ranges from 0 (objective) to 1 (subjective)
        - **Fast Processing**: Real-time analysis with minimal latency
        - **Language Support**: Optimized for English text
        
        ### Classification Thresholds:
        - **Positive**: Polarity ≥ 0.1
        - **Neutral**: Polarity between -0.1 and 0.1
        - **Negative**: Polarity ≤ -0.1
        
        ### Confidence Calculation:
        Confidence is calculated based on:
        1. Magnitude of polarity (strength of sentiment)
        2. Subjectivity score (subjective text has clearer sentiment)
        3. Combined weighted score normalized to 0-100%
        """)
    
    st.markdown("---")
    
    # Examples
    st.markdown("## 📚 Example Analyses")
    st.markdown("Here are some examples of how SentimentScope classifies different texts:")
    
    # Create example table
    examples_data = {
        "Text": [
            "I love this product! It's absolutely amazing and worth every penny.",
            "The service was okay, nothing special but not bad either.",
            "This is the worst experience I've ever had. Completely disappointed.",
            "The package arrived on time and contained all items.",
            "I'm thrilled with the results! Exceeded all my expectations.",
            "Terrible quality, would not recommend to anyone.",
            "It works as described in the specifications.",
            "Outstanding service! The team went above and beyond."
        ],
        "Sentiment": [
            "😊 Positive",
            "😐 Neutral",
            "😠 Negative",
            "😐 Neutral",
            "😊 Positive",
            "😠 Negative",
            "😐 Neutral",
            "😊 Positive"
        ],
        "Confidence": [
            "~95%",
            "~45%",
            "~98%",
            "~35%",
            "~92%",
            "~88%",
            "~40%",
            "~94%"
        ]
    }
    
    st.table(examples_data)
    
    st.markdown("---")
    
    # Use Cases
    st.markdown("## 🚀 Use Cases")
    
    use_case_cols = st.columns(3)
    
    with use_case_cols[0]:
        st.markdown("""
        ### 🏢 Business
        - Customer feedback analysis
        - Brand monitoring
        - Market research
        - Product review analysis
        - Employee satisfaction surveys
        """)
    
    with use_case_cols[1]:
        st.markdown("""
        ### 📱 Social Media
        - Twitter sentiment tracking
        - Facebook comment analysis
        - Instagram caption analysis
        - Reddit post sentiment
        - YouTube comment analysis
        """)
    
    with use_case_cols[2]:
        st.markdown("""
        ### 📧 Communication
        - Email sentiment detection
        - Chat message analysis
        - Support ticket prioritization
        - Content moderation
        - Survey response analysis
        """)
    
    st.markdown("---")
    
    # Features
    st.markdown("## ✨ Key Features")
    
    feature_cols = st.columns(2)
    
    with feature_cols[0]:
        st.markdown("""
        ### Current Features:
        - ✅ Real-time sentiment analysis
        - ✅ Confidence scoring
        - ✅ Visual polarity gauge
        - ✅ Analysis history tracking
        - ✅ Export results to file
        - ✅ Quick example templates
        - ✅ Character & word counter
        - ✅ Detailed metrics display
        """)
    
    with feature_cols[1]:
        st.markdown("""
        ### 🔮 Coming Soon:
        - 🔄 Batch CSV file analysis
        - 🌍 Multi-language support
        - 🎭 Emotion detection
        - 🔑 Keyword extraction
        - 📊 Advanced analytics dashboard
        - 🔗 API integration
        - 📈 Sentiment trends over time
        - 👥 Team collaboration features
        """)
    
    st.markdown("---")
    
    # Technology Stack
    st.markdown("## 🛠️ Technology Stack")
    
    tech_cols = st.columns(4)
    
    with tech_cols[0]:
        st.markdown("""
        ### Frontend
        - Streamlit
        - Plotly
        - CSS
        """)
    
    with tech_cols[1]:
        st.markdown("""
        ### NLP/ML
        - TextBlob
        - NLTK
        - Python 3.10+
        """)
    
    with tech_cols[2]:
        st.markdown("""
        ### UI Components
        - streamlit-option-menu
        - streamlit-extras
        """)
    
    with tech_cols[3]:
        st.markdown("""
        ### Deployment
        - Streamlit Cloud
        - GitHub
        - Docker (optional)
        """)
    
    st.markdown("---")
    
    # Security Features
    st.markdown("## 🛡️ Security & Privacy")
    
    security_cols = st.columns(2)
    
    with security_cols[0]:
        st.markdown("""
        ### Security Features:
        - ✅ **Input Validation** - All text is validated and sanitized
        - ✅ **Rate Limiting** - Prevents abuse (10/min, 100/hour)
        - ✅ **XSS Protection** - HTML/Script tags removed
        - ✅ **SQL Injection Prevention** - Malicious patterns blocked
        - ✅ **Spam Detection** - Automated spam filtering
        - ✅ **Length Limits** - Maximum 10,000 characters
        - ✅ **Session Management** - Secure session handling
        """)
    
    with security_cols[1]:
        st.markdown("""
        ### Privacy Guarantee:
        - 🔒 **No Data Storage** - Nothing saved to servers
        - 🔒 **Local Processing** - All analysis done in your session
        - 🔒 **No Tracking** - No personal data collected
        - 🔒 **Session Only** - History cleared on exit
        - 🔒 **No Third-Party** - No external API calls
        - 🔒 **Open Source** - Code is transparent
        - 🔒 **MIT Licensed** - Free and open
        """)
    
    st.markdown("---")
    
    # Limitations
    st.markdown("## ⚠️ Limitations & Considerations")
    
    st.warning("""
    ### Current Limitations:
    
    1. **Language**: Optimized for English text. Other languages may produce less accurate results.
    
    2. **Context**: Cannot understand complex context, sarcasm, or irony perfectly.
    
    3. **Domain**: Works best on general text. Specialized domains (medical, legal) may need custom models.
    
    4. **Length**: Very short texts (< 5 words) may have lower accuracy.
    
    5. **Emojis**: Basic emoji support. Complex emoji combinations might not be fully interpreted.
    """)
    
    st.markdown("---")
    
    # FAQ
    st.markdown("## ❓ Frequently Asked Questions")
    
    with st.expander("Is my data stored or shared?"):
        st.markdown("""
        No, SentimentScope processes all text locally in your session. No data is stored on servers 
        or shared with third parties. Analysis history is kept only in your current browser session 
        and cleared when you close the app.
        """)
    
    with st.expander("How accurate is the sentiment analysis?"):
        st.markdown("""
        TextBlob typically achieves 70-80% accuracy on general text. Accuracy varies based on:
        - Text complexity and length
        - Presence of sarcasm or irony
        - Domain-specific language
        - Grammatical correctness
        
        For production applications requiring higher accuracy, consider using transformer-based 
        models like BERT or RoBERTa.
        """)
    
    with st.expander("Can I analyze text in languages other than English?"):
        st.markdown("""
        Currently, SentimentScope is optimized for English text. While it may work with other 
        languages, accuracy will be significantly lower. Multi-language support is planned for 
        future updates.
        """)
    
    with st.expander("What's the maximum text length I can analyze?"):
        st.markdown("""
        There's no strict limit, but for best performance and accuracy, we recommend:
        - **Minimum**: 10 words
        - **Optimal**: 20-500 words
        - **Maximum**: 5000 words
        
        Very long texts can be analyzed in batches for better results.
        """)
    
    with st.expander("Can I integrate SentimentScope into my application?"):
        st.markdown("""
        The core sentiment analysis logic can be extracted and used in your own applications.
        API integration and webhook support are planned for future releases. For custom 
        integration needs, you can use the open-source codebase.
        """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("## 📬 Feedback & Support")
    
    st.info("""
    We're constantly improving SentimentScope! If you have suggestions, feature requests, 
    or encounter any issues, please let us know.
    
    **Developer:** Ishan Chakraborty
    
    **Contact:** [ishanrock1234@gmail.com](mailto:ishanrock1234@gmail.com)
    
    **GitHub:** [Ishan96Dev](https://github.com/Ishan96Dev)
    
    **License:** MIT License - Free and Open Source
    """)
    
    st.success("""
    ### 🌟 Thank you for using SentimentScope!
    
    **Created by: Ishan Chakraborty**
    
    Built with ❤️ using Streamlit and Natural Language Processing.
    
    © 2026 SentimentScope | MIT License
    """)