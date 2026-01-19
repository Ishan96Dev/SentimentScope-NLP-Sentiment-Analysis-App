# SentimentScope - Developer Quick Reference Card

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -m textblob.download_corpora

# Run app
streamlit run app.py

# App will open at: http://localhost:8501
```

---

## 📁 Project Structure

```
├── app.py                 # Main entry point (121 lines)
├── sentiment/
│   └── analyzer.py        # NLP engine (200 lines)
├── ui/
│   ├── home.py           # Main interface (293 lines)
│   └── about.py          # Info page (396 lines)
├── utils/
│   └── security.py       # Security utilities (295 lines)
├── DOCUMENTATION.md      # Complete reference (600+ lines)
└── DOCUMENTATION_SUMMARY.md  # This file
```

---

## 🔑 Key Classes & Functions

### Sentiment Analysis

```python
# Get analyzer instance (singleton)
from sentiment.analyzer import get_analyzer
analyzer = get_analyzer()

# Analyze single text
result = analyzer.analyze("I love this product!")
# Returns: {label, confidence, polarity, subjectivity, emoji, color, ...}

# Batch analyze
texts = ["Text 1", "Text 2", "Text 3"]
results = analyzer.batch_analyze(texts)
```

### Security Validation

```python
from utils.security import InputValidator, RateLimiter

# Validate input
is_valid, error = InputValidator.validate_input(text)
if not is_valid:
    print(error)

# Sanitize text
clean_text = InputValidator.sanitize_text(text)

# Check spam
is_spam = InputValidator.is_spam(text)

# Check rate limit
is_allowed, message = RateLimiter.check_rate_limit()
```

### Session Management

```python
from utils.security import SessionManager

# Initialize session
SessionManager.initialize_session()

# Check validity
is_valid = SessionManager.check_session_validity()

# Refresh session
SessionManager.refresh_session()
```

---

## 📊 Sentiment Classification

| Polarity Range | Label | Emoji | Color |
|----------------|-------|-------|-------|
| >= 0.1 | Positive | 😊 | #10b981 (green) |
| -0.1 to 0.1 | Neutral | 😐 | #f59e0b (orange) |
| <= -0.1 | Negative | 😠 | #ef4444 (red) |

---

## 🔒 Security Limits

| Feature | Limit | Purpose |
|---------|-------|---------|
| **Min Text Length** | 1 character | Prevent empty input |
| **Max Text Length** | 10,000 characters | Prevent DoS |
| **Max Word Count** | 2,000 words | Prevent memory issues |
| **Requests/Minute** | 10 | Rate limiting |
| **Requests/Hour** | 100 | Rate limiting |
| **Cooldown** | 2 seconds | Anti-spam |
| **Session Timeout** | 60 minutes | Security |
| **History Size** | 10 entries | Memory management |
| **Log Size** | 100 entries | Memory management |

---

## 🧪 Testing Examples

```python
# Positive sentiment
analyzer.analyze("I absolutely love this! Amazing experience!")
# Expected: label="Positive", confidence ~85-95%

# Negative sentiment
analyzer.analyze("This is terrible and disappointing.")
# Expected: label="Negative", confidence ~80-90%

# Neutral sentiment
analyzer.analyze("The package arrived on time.")
# Expected: label="Neutral", confidence ~40-60%

# Edge cases
analyzer.analyze("")  # Raises ValueError: "Text input cannot be empty"
analyzer.analyze("a" * 10001)  # Raises ValueError: "Text is too long"
analyzer.analyze("<script>alert('xss')</script>")  # Sanitized and analyzed
```

---

## 🎯 Confidence Formula

```
confidence = |polarity| × 100 × (0.3 + subjectivity × 0.7)

Components:
- |polarity| × 100: Base confidence (0-100)
- 0.3 + subjectivity × 0.7: Adjustment factor (0.3-1.0)

Examples:
- polarity=0.8, subjectivity=0.9 → confidence=72%
- polarity=0.2, subjectivity=0.3 → confidence=10.2%
- polarity=-0.5, subjectivity=0.6 → confidence=32.5%
```

---

## 🛡️ Security Patterns

### XSS Prevention
```python
# Remove script tags
text = re.sub(r'<script[^>]*>.*?</script>', '', text)

# Remove all HTML tags
text = re.sub(r'<[^>]+>', '', text)
```

### SQL Injection Detection
```python
# Detect SQL keywords
pattern = r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)"
if re.search(pattern, text, re.IGNORECASE):
    # Block request
```

### Spam Detection
```python
# Check for spam indicators
spam_patterns = [
    r'(viagra|cialis|lottery|winner)',
    r'(\$\$\$|!!!!!!)',
    r'(http[s]?://.*){5,}'  # Too many URLs
]
```

---

## 📈 Result Dictionary Structure

```python
{
    "label": "Positive",           # str: Sentiment label
    "confidence": 87.5,            # float: 0-100%
    "polarity": 0.750,             # float: -1.0 to +1.0
    "subjectivity": 0.900,         # float: 0.0 to 1.0
    "emoji": "😊",                 # str: Visual indicator
    "color": "#10b981",            # str: Hex color code
    "text_length": 42,             # int: Character count
    "word_count": 7                # int: Word count
}
```

---

## 🔄 Analysis Flow

```
User Input
    ↓
Empty Check → Error if empty
    ↓
Input Validation → Error if invalid
    ↓
Rate Limit Check → Warning if exceeded
    ↓
Text Sanitization
    ↓
Spam Check → Error if spam
    ↓
TextBlob Analysis
    ↓
Classification (Positive/Neutral/Negative)
    ↓
Confidence Calculation
    ↓
Results Display
```

---

## 🎨 UI Color Scheme

```css
/* Primary Brand Color */
#667eea  /* Purple - menu, buttons */

/* Sentiment Colors */
#10b981  /* Green - Positive */
#f59e0b  /* Orange - Neutral */
#ef4444  /* Red - Negative */

/* Gradients */
Positive: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Negative: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)
Neutral:  linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)
```

---

## 📝 Session State Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `history` | list | Last 10 analyses |
| `analysis_count` | int | Total analyses this session |
| `session_initialized` | bool | Session setup flag |
| `session_start_time` | datetime | Session creation time |
| `session_id` | str | Unique session identifier |
| `rate_limit_requests` | list | Request timestamps |
| `last_request_time` | float | Last request time |
| `security_logs` | list | Last 100 log entries |
| `example_text` | str | Selected example text |

---

## 🚨 Common Errors & Solutions

### Error: "Text input cannot be empty"
**Cause:** Empty or whitespace-only text  
**Solution:** Enter valid text

### Error: "Text is too long. Maximum 10,000 characters allowed"
**Cause:** Text exceeds length limit  
**Solution:** Reduce text length or split into batches

### Warning: "Rate limit exceeded"
**Cause:** Too many requests (>10/min or >100/hour)  
**Solution:** Wait before trying again

### Error: "Spam content detected"
**Cause:** Text matches spam patterns  
**Solution:** Remove spam indicators

### Error: "Invalid input detected"
**Cause:** SQL keywords or excessive special characters  
**Solution:** Remove SQL keywords or special characters

---

## 🔧 Customization Points

### Modify Thresholds
```python
# In sentiment/analyzer.py
POSITIVE_THRESHOLD = 0.1  # Change for more/less strict
NEGATIVE_THRESHOLD = -0.1
```

### Adjust Rate Limits
```python
# In utils/security.py
MAX_REQUESTS_PER_MINUTE = 10  # Increase for more lenient
MAX_REQUESTS_PER_HOUR = 100
COOLDOWN_SECONDS = 2
```

### Change Confidence Formula
```python
# In sentiment/analyzer.py - _calculate_confidence()
subjectivity_factor = 0.3 + (subjectivity * 0.7)
# Adjust weights: 0.3 (minimum) and 0.7 (maximum multiplier)
```

---

## 📊 Performance Tips

1. **Use Singleton:** Always use `get_analyzer()` (don't create new instances)
2. **Batch Processing:** Use `batch_analyze()` for multiple texts
3. **Limit History:** Keep history at 10 entries max
4. **Clear Logs:** Periodically clear security logs
5. **Text Length:** Process shorter texts (<1000 chars) for speed

---

## 🧰 Debugging

### Enable Debug Mode
```python
# In app.py, add after imports:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### View Session State
```python
# In any screen, add:
st.write(st.session_state)
```

### Check Security Logs
```python
# In home.py, add:
from utils.security import SecurityLogger
logs = SecurityLogger.get_recent_logs(10)
st.write(logs)
```

---

## 📚 Documentation Files

- **DOCUMENTATION.md**: Complete reference guide (600+ lines)
- **DOCUMENTATION_SUMMARY.md**: Status and coverage report
- **README.md**: Project overview and setup
- **SECURITY.md**: Security policy and features
- **LICENSE**: MIT License text

---

## 🔗 Useful Commands

```bash
# Run app
streamlit run app.py

# Run on specific port
streamlit run app.py --server.port 8502

# Run with live reloading
streamlit run app.py --server.runOnSave true

# Check Streamlit version
streamlit version

# Update dependencies
pip install -r requirements.txt --upgrade

# Freeze dependencies
pip freeze > requirements.txt
```

---

## 📞 Support & Contact

**Author:** Ishan Chakraborty  
**Email:** ishanrock1234@gmail.com  
**GitHub:** [@Ishan96Dev](https://github.com/Ishan96Dev)  
**License:** MIT  
**Version:** 1.0.0  
**Last Updated:** January 19, 2026

---

## ✅ Pre-Deployment Checklist

- [ ] All dependencies installed
- [ ] NLTK data downloaded
- [ ] App runs locally without errors
- [ ] Security features tested
- [ ] Rate limiting verified
- [ ] All documentation complete
- [ ] README.md updated
- [ ] LICENSE file present
- [ ] Git repository initialized
- [ ] .gitignore configured

---

**Quick Tip:** Keep this file open while developing for fast reference to APIs, limits, and patterns!
