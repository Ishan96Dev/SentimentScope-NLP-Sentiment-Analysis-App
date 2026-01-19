# SentimentScope - Complete Code Documentation

## Table of Contents
1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Module Documentation](#module-documentation)
4. [Function Reference](#function-reference)
5. [Security Features](#security-features)
6. [Code Flow](#code-flow)

---

## Overview

SentimentScope is a professional NLP-based sentiment analysis web application built with Streamlit and TextBlob. The application provides real-time sentiment detection with comprehensive security features, rate limiting, and user-friendly interface.

**Author:** Ishan Chakraborty  
**Email:** ishanrock1234@gmail.com  
**GitHub:** @Ishan96Dev  
**License:** MIT  
**Copyright:** © 2026

---

## File Structure

```
Streamlit-Sentiment-Analysis-App/
├── app.py                      # Main application entry point
├── sentiment/
│   ├── __init__.py            # Package initialization
│   └── analyzer.py            # Core sentiment analysis engine
├── ui/
│   ├── __init__.py            # Package initialization
│   ├── home.py                # Main analyzer interface
│   └── about.py               # Application information page
├── utils/
│   ├── __init__.py            # Package initialization
│   └── security.py            # Security and validation utilities
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── LICENSE                    # MIT License
├── SECURITY.md               # Security policy
└── DOCUMENTATION.md          # This file - complete documentation
```

---

## Module Documentation

### 1. app.py - Main Application Entry Point

**Purpose:** Application initialization, configuration, navigation, and layout

**Key Responsibilities:**
- Initialize security session
- Configure Streamlit page settings
- Apply custom CSS styling
- Render sidebar navigation menu
- Display usage statistics
- Route to appropriate screens
- Show application footer

**Main Components:**

#### Session Initialization
```python
SessionManager.initialize_session()
```
- Sets up secure session tracking
- Creates unique session ID
- Initializes session start time
- Prepares session state variables

#### Page Configuration
```python
st.set_page_config(
    page_title="SentimentScope - Sentiment Analysis",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
```
- **page_title:** Browser tab title
- **page_icon:** Brain emoji (🧠) represents AI/NLP
- **layout:** "wide" uses full browser width
- **initial_sidebar_state:** Sidebar visible by default

#### Custom CSS
Applies professional styling for:
- Main content padding (2rem = 32px)
- Full-width buttons with rounded corners
- Sentiment cards with gradient backgrounds
  - Positive: Purple gradient (#667eea → #764ba2)
  - Negative: Pink/red gradient (#f093fb → #f5576c)
  - Neutral: Blue/cyan gradient (#4facfe → #00f2fe)

#### Navigation Menu
```python
selected = option_menu(
    menu_title=None,
    options=["Sentiment Analyzer", "About App"],
    icons=["brain", "info-circle"],
    default_index=0,
    styles={...}
)
```
- Interactive sidebar menu using `streamlit-option-menu`
- Two main screens: Home (analyzer) and About
- Custom purple theme (#667eea)
- Bootstrap icons for visual appeal

#### Usage Statistics
Displays in sidebar:
- **Analysis Count:** Total analyses performed this session
- **Rate Limits:** Remaining requests per minute and hour

#### Screen Routing
```python
if selected == "Sentiment Analyzer":
    home.render()
elif selected == "About App":
    about.render()
```
Calls appropriate render function based on menu selection

---

### 2. sentiment/analyzer.py - Core NLP Engine

**Purpose:** Sentiment analysis using TextBlob NLP library

**Key Responsibilities:**
- Text preprocessing and sanitization
- Sentiment polarity calculation (-1 to +1)
- Subjectivity analysis (0 to 1)
- Sentiment classification (Positive/Neutral/Negative)
- Confidence score calculation (0-100%)
- Batch processing support
- Security validation

**Main Class: SentimentAnalyzer**

#### Constants
```python
POSITIVE_THRESHOLD = 0.1   # polarity >= 0.1 is positive
NEGATIVE_THRESHOLD = -0.1  # polarity <= -0.1 is negative
```
Values between -0.1 and 0.1 are considered neutral

#### Method: preprocess_text(text)
**Purpose:** Clean and sanitize text for safe analysis

**Steps:**
1. **HTML Entity Decoding**
   ```python
   text = html.unescape(text)
   ```
   Converts `&lt;` → `<`, `&amp;` → `&`, etc.

2. **Whitespace Normalization**
   ```python
   text = re.sub(r'\s+', ' ', text).strip()
   ```
   Replaces multiple spaces/tabs/newlines with single space

3. **Dangerous Character Removal**
   ```python
   text = re.sub(r'[^\w\s\.\!\?\,\;\:\-\']', '', text)
   ```
   Keeps only alphanumeric, whitespace, and basic punctuation
   Blocks: `<`, `>`, `{`, `}`, `[`, `]`, `(`, `)`, etc.

4. **Repeated Character Limiting**
   ```python
   text = re.sub(r'(.)\1{4,}', r'\1\1\1', text)
   ```
   Anti-spam: "loooooove" → "looove" (max 3 repetitions)

**Security Protection:**
- XSS (Cross-Site Scripting) prevention
- Code injection blocking
- Spam detection
- HTML/JavaScript filtering

#### Method: analyze(text)
**Purpose:** Main analysis method returning comprehensive results

**Validation Checks:**
1. Empty text detection
2. Maximum length: 10,000 characters
3. Maximum words: 2,000 words

**Analysis Pipeline:**
```
Input Text
    ↓
Validation
    ↓
Preprocessing
    ↓
TextBlob Analysis
    ↓
Classification
    ↓
Confidence Calculation
    ↓
Results Dictionary
```

**Return Dictionary:**
```python
{
    "label": str,           # "Positive", "Neutral", "Negative"
    "confidence": float,    # 0-100% confidence score
    "polarity": float,      # -1.0 to +1.0 sentiment polarity
    "subjectivity": float,  # 0.0 to 1.0 subjectivity score
    "emoji": str,           # 😊, 😐, or 😠
    "color": str,           # Hex color code for UI
    "text_length": int,     # Character count
    "word_count": int       # Word count
}
```

#### Method: _classify_sentiment(polarity)
**Purpose:** Determine sentiment category from polarity

**Logic:**
```python
if polarity >= 0.1:
    return "Positive", "😊", "#10b981"   # Green
elif polarity <= -0.1:
    return "Negative", "😠", "#ef4444"   # Red
else:
    return "Neutral", "😐", "#f59e0b"    # Orange
```

#### Method: _calculate_confidence(polarity, subjectivity)
**Purpose:** Calculate confidence score (0-100%)

**Formula:**
```
confidence = |polarity| × 100 × (0.3 + subjectivity × 0.7)
```

**Components:**
1. **Polarity Magnitude:** `abs(polarity) × 100`
   - Stronger sentiment = higher confidence
   - Example: polarity of ±0.8 gives base of 80%

2. **Subjectivity Factor:** `0.3 + subjectivity × 0.7`
   - Range: [0.3, 1.0]
   - More subjective text = clearer sentiment
   - Minimum 30% factor for objective text

**Example Calculations:**
- `polarity=0.8, subjectivity=0.9`: confidence = 72%
- `polarity=0.2, subjectivity=0.3`: confidence = 10.2%
- `polarity=-0.5, subjectivity=0.6`: confidence = 32.5%

#### Method: batch_analyze(texts)
**Purpose:** Analyze multiple texts in one operation

**Features:**
- Processes texts sequentially
- Error handling per text (doesn't stop on failure)
- Returns list of results
- Includes original text in results

**Use Cases:**
- Bulk customer feedback analysis
- Social media post processing
- Survey response analysis
- CSV file batch processing

#### Function: get_analyzer()
**Purpose:** Singleton pattern - reuse analyzer instance

**Benefits:**
- Memory efficiency (single instance)
- No repeated initialization
- State consistency across app

---

### 3. utils/security.py - Security Utilities

**Purpose:** Comprehensive security validation, rate limiting, logging, and session management

---

#### Class: InputValidator

**Purpose:** Validate and sanitize user input

**Security Limits:**
```python
MIN_TEXT_LENGTH = 1
MAX_TEXT_LENGTH = 10000  # 10k characters
MAX_WORD_COUNT = 2000
```

**Security Patterns:**
```python
SCRIPT_PATTERN = re.compile(r'<script[^>]*>.*?</script>')
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
SQL_INJECTION_PATTERN = re.compile(
    r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)",
    re.IGNORECASE
)
```

**Method: sanitize_text(text)**
Steps:
1. Remove `<script>` tags
2. Remove all HTML tags
3. Limit to MAX_TEXT_LENGTH
4. Trim whitespace

**Method: validate_input(text)**
Checks:
1. Non-empty text
2. Minimum length (1 character)
3. Maximum length (10,000 characters)
4. Maximum words (2,000 words)
5. SQL injection patterns
6. Special character ratio (< 50%)

Returns: `(is_valid, error_message)`

**Method: is_spam(text)**
Detects spam indicators:
- Spam keywords: viagra, lottery, winner, etc.
- Excessive punctuation: $$$ or !!!!!!
- Too many URLs (5+ links)

---

#### Class: RateLimiter

**Purpose:** Prevent abuse through rate limiting

**Limits:**
```python
MAX_REQUESTS_PER_MINUTE = 10
MAX_REQUESTS_PER_HOUR = 100
COOLDOWN_SECONDS = 2
```

**Method: check_rate_limit()**
**Logic:**
1. Initialize session tracking if not exists
2. Remove requests older than 1 hour
3. Check cooldown period (2 seconds)
4. Check per-minute limit (10 requests)
5. Check per-hour limit (100 requests)
6. Update tracking if allowed

**Returns:** `(is_allowed, error_message)`

**Session State Variables:**
- `rate_limit_requests`: List of timestamps
- `last_request_time`: Last request timestamp

**Method: get_usage_stats()**
Returns dictionary:
```python
{
    'requests_last_minute': int,
    'requests_last_hour': int,
    'remaining_minute': int,
    'remaining_hour': int
}
```

---

#### Class: SecurityLogger

**Purpose:** Log security events for monitoring

**Method: log_event(event_type, details)**
Creates log entry:
```python
{
    'timestamp': '2026-01-19T10:30:00.123456',
    'type': 'validation_error',
    'details': 'Text too long'
}
```

**Storage:** In-memory (last 100 entries)

**Event Types:**
- `validation_error`: Input validation failures
- `rate_limit`: Rate limit exceeded
- `spam_detected`: Spam content blocked
- `analysis_success`: Successful analysis
- `analysis_error`: Analysis failed

**Method: get_recent_logs(count=10)**
Returns list of recent log entries

---

#### Class: SessionManager

**Purpose:** Secure session management

**Configuration:**
```python
SESSION_TIMEOUT_MINUTES = 60
```

**Method: initialize_session()**
Sets up:
```python
session_initialized = True
session_start_time = datetime.now()
session_id = "session_{timestamp_ms}"
```

**Method: check_session_validity()**
Validates:
1. Session exists
2. Session age < 60 minutes

Returns: `True` if valid, `False` otherwise

**Method: refresh_session()**
Updates `session_start_time` to current time

---

### 4. ui/home.py - Main Analyzer Interface

**Purpose:** User interface for sentiment analysis

**Key Components:**

#### Header Section
```python
st.markdown("# 🧠 Sentiment Analyzer")
st.markdown("### Analyze text sentiment with AI-powered NLP")
```

#### Session State Initialization
```python
if "history" not in st.session_state:
    st.session_state.history = []
```
Stores last 10 analyses

#### Two-Column Layout
- **Left Column:** Input area, examples, analysis
- **Right Column:** Instructions, info panel

#### Quick Example Buttons
Three pre-filled examples:
1. **Positive:** "I absolutely loved this experience!"
2. **Neutral:** "The product arrived on time."
3. **Negative:** "This is the worst service..."

#### Text Input Area
```python
text_input = st.text_area(
    label="Text to analyze",
    height=200,
    placeholder="Enter your text here..."
)
```

#### Character Counter
Displays:
- Character count
- Word count

#### Analysis Button Logic

**Security Flow:**
```
User clicks "Analyze"
    ↓
Check if text is empty
    ↓
Validate input (InputValidator)
    ↓
Check rate limit (RateLimiter)
    ↓
Sanitize text (InputValidator)
    ↓
Check for spam
    ↓
Analyze sentiment (SentimentAnalyzer)
    ↓
Display results
```

**Error Handling:**
- Empty input: Show error
- Validation failure: Show error message
- Rate limit exceeded: Show warning
- Spam detected: Show error
- Analysis error: Catch and log exception

#### Results Display

**Main Result Card:**
- Large emoji (5em font size)
- Sentiment label
- Confidence percentage with progress bar
- Polarity and subjectivity metrics

**Detailed Metrics:**
Four columns showing:
1. Sentiment label
2. Confidence percentage
3. Character count
4. Word count

**Gauge Chart:**
Plotly gauge visualization:
- Value: Polarity score
- Range: -1 to +1
- Color-coded sections:
  - Red zone: -1 to -0.1 (negative)
  - Yellow zone: -0.1 to 0.1 (neutral)
  - Green zone: 0.1 to 1 (positive)
- Dynamic needle color based on sentiment

**Interpretation:**
Contextual message based on sentiment:
- **Positive:** Success box with green background
- **Negative:** Error box with red background
- **Neutral:** Warning box with yellow background

**Export Functionality:**
Download button creates text report:
```
Sentiment Analysis Report
========================
Text: {first 200 characters}...
Sentiment: Positive
Confidence: 87.5%
Polarity: 0.750
Subjectivity: 0.900
Timestamp: 2026-01-19 10:30:00
```

#### History Section
Shows last 5 analyses in expandable panel:
- Truncated text (100 characters)
- Sentiment label with emoji
- Confidence percentage
- Timestamp

**Clear History Button:**
Empties history and refreshes page

---

### 5. ui/about.py - Application Information

**Purpose:** Documentation and information page

**Sections:**

1. **Header:** App name and tagline
2. **Introduction:** What is SentimentScope
3. **What is Sentiment Analysis:** Educational content
4. **How It Works:** 4-step process visualization
5. **Technical Details:** TextBlob info, thresholds, formulas
6. **Example Analyses:** Sample text/sentiment table
7. **Use Cases:** Business, social media, communication
8. **Key Features:** Current and planned features
9. **Technology Stack:** Frontend, NLP, UI, deployment
10. **Security & Privacy:** Security features and guarantees
11. **Limitations:** Current constraints and considerations
12. **FAQ:** Common questions and answers
13. **Feedback & Support:** Contact information

**Interactive Elements:**
- Expandable sections (expanders)
- Multi-column layouts
- Color-coded information boxes
- Tables for examples
- Icons and emojis for visual appeal

---

## Function Reference

### Sentiment Analysis Functions

#### `get_analyzer() -> SentimentAnalyzer`
Returns singleton analyzer instance

#### `SentimentAnalyzer.analyze(text: str) -> Dict`
Analyzes text and returns comprehensive results

#### `SentimentAnalyzer.batch_analyze(texts: list) -> list`
Analyzes multiple texts in batch

#### `SentimentAnalyzer.preprocess_text(text: str) -> str`
Cleans and sanitizes text

### Security Functions

#### `InputValidator.validate_input(text: str) -> Tuple[bool, Optional[str]]`
Validates text input, returns (is_valid, error_message)

#### `InputValidator.sanitize_text(text: str) -> str`
Removes dangerous content from text

#### `InputValidator.is_spam(text: str) -> bool`
Checks if text is spam

#### `RateLimiter.check_rate_limit() -> Tuple[bool, Optional[str]]`
Checks rate limits, returns (is_allowed, message)

#### `RateLimiter.get_usage_stats() -> dict`
Returns current usage statistics

#### `SecurityLogger.log_event(event_type: str, details: str)`
Logs security event

#### `SecurityLogger.get_recent_logs(count: int = 10) -> list`
Returns recent log entries

#### `SessionManager.initialize_session()`
Initializes secure session

#### `SessionManager.check_session_validity() -> bool`
Checks if session is valid

#### `SessionManager.refresh_session()`
Refreshes session timestamp

### UI Rendering Functions

#### `home.render()`
Renders main sentiment analyzer interface

#### `about.render()`
Renders about/information page

---

## Security Features

### Input Validation
- **Length Limits:** 1-10,000 characters, max 2,000 words
- **Content Filtering:** XSS, SQL injection, HTML tags
- **Character Validation:** Special character ratio check
- **Spam Detection:** Pattern-based spam filtering

### Rate Limiting
- **Per-Minute:** 10 requests maximum
- **Per-Hour:** 100 requests maximum
- **Cooldown:** 2 seconds between requests
- **Session-Based:** Tracked per browser session

### Sanitization
- **HTML Entity Decoding:** Prevent entity-based attacks
- **Tag Removal:** Strip all HTML tags
- **Script Blocking:** Remove `<script>` elements
- **Character Filtering:** Allow only safe characters

### Session Security
- **Timeout:** 60-minute session expiry
- **Unique IDs:** Timestamp-based session identifiers
- **State Management:** Secure session state tracking
- **Auto-Refresh:** Session renewal on activity

### Logging
- **Event Tracking:** All security events logged
- **Audit Trail:** Timestamp and details recorded
- **Error Capture:** Validation and analysis errors logged
- **Memory Management:** Last 100 entries kept

---

## Code Flow

### Application Startup
```
1. Import modules
2. Initialize security session (SessionManager)
3. Configure Streamlit page
4. Apply custom CSS
5. Render sidebar navigation
6. Route to selected screen (home or about)
7. Display footer
```

### Analysis Flow
```
1. User enters text
2. User clicks "Analyze" button
3. Check if text is empty → Error if empty
4. Validate input (InputValidator) → Error if invalid
5. Check rate limit (RateLimiter) → Warning if exceeded
6. Sanitize text (InputValidator)
7. Check for spam → Error if spam detected
8. Analyze sentiment (TextBlob)
9. Calculate confidence score
10. Classify sentiment (Positive/Neutral/Negative)
11. Display results (emoji, metrics, gauge, interpretation)
12. Add to history (last 10)
13. Increment analysis counter
14. Log success event
```

### Error Handling Flow
```
1. Try to analyze text
2. Catch ValueError (validation errors)
   → Display error message
   → Log validation error
3. Catch Exception (unexpected errors)
   → Display generic error message
   → Log analysis error
4. Continue (don't crash app)
```

### Session Management Flow
```
1. Initialize session on app start
2. Check validity before operations
3. Refresh session on user activity
4. Timeout after 60 minutes of inactivity
5. Clear session state on timeout
```

---

## Performance Considerations

### Analysis Speed
- **Single text:** ~10-50ms (TextBlob processing)
- **Batch (100 texts):** ~1-5 seconds
- **Large text (10k chars):** ~50-100ms

### Memory Usage
- **Analyzer:** <1MB (stateless)
- **Session state:** ~1KB per session
- **History:** ~10KB (last 10 analyses)
- **Logs:** ~10KB (last 100 entries)

### Optimization Tips
1. Use singleton analyzer (avoid re-initialization)
2. Batch process when possible
3. Keep history limited (10 entries)
4. Clear logs periodically
5. Limit text length for faster processing

---

## Testing Recommendations

### Unit Tests
- Test each analyzer method independently
- Test validation rules
- Test rate limiting logic
- Test confidence calculations

### Integration Tests
- Test full analysis pipeline
- Test UI rendering
- Test session management
- Test error handling

### Security Tests
- Test XSS prevention
- Test SQL injection blocking
- Test spam detection
- Test rate limit enforcement

### Example Test Cases
```python
# Positive sentiment
"I absolutely love this product! It's amazing!"

# Negative sentiment
"This is terrible and disappointing."

# Neutral sentiment
"The package arrived on time."

# Edge cases
"" # Empty
"a" * 10001 # Too long
"<script>alert('xss')</script>" # XSS attempt
"SELECT * FROM users" # SQL injection attempt
```

---

## Deployment Notes

### Requirements
- Python 3.8+
- Streamlit 1.52+
- TextBlob 0.19+
- NLTK 3.9.2+
- Plotly 6.5.2+

### Environment Setup
```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

### Running Locally
```bash
streamlit run app.py
```

### Cloud Deployment
- Streamlit Cloud: Automatic deployment from GitHub
- Heroku: Use Procfile
- AWS/Azure: Use container deployment

### Configuration
- No environment variables required
- No external API keys needed
- No database setup required
- Self-contained application

---

## Maintenance

### Regular Tasks
1. Monitor error logs
2. Review rate limit effectiveness
3. Update spam patterns
4. Optimize confidence formula
5. Update dependencies

### Known Issues
- Sarcasm detection limited
- Language support: English only
- Short text accuracy lower
- Emoji interpretation basic

### Future Enhancements
- Multi-language support
- Emotion detection
- Keyword extraction
- Batch CSV processing
- API integration
- Advanced analytics
- Team features

---

## License

MIT License - Free and open source  
Copyright (c) 2026 Ishan Chakraborty

---

**Last Updated:** January 19, 2026  
**Version:** 1.0.0  
**Author:** Ishan Chakraborty  
**Contact:** ishanrock1234@gmail.com
