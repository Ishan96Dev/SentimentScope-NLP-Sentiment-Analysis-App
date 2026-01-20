# 🛡️ Security & Privacy Policy

**SentimentScope - Security Documentation**  
**Author:** Ishan Chakraborty  
**Last Updated:** January 19, 2026

---

## 🔒 Overview

SentimentScope takes security and privacy seriously. This document outlines all security measures, privacy policies, and best practices implemented in the application.

---

## 🛡️ Security Features

### 1. Input Validation & Sanitization

#### Validation Rules:
- **Minimum Length:** 1 character
- **Maximum Length:** 10,000 characters
- **Maximum Words:** 2,000 words
- **Special Character Ratio:** Max 50% of content

#### Sanitization Process:
- HTML entity decoding
- Script tag removal
- HTML tag stripping
- SQL keyword detection
- Excessive special character filtering
- Repeated character limiting

#### Code Implementation:
```python
from utils.security import InputValidator

# Validate input
is_valid, error = InputValidator.validate_input(text)

# Sanitize input
clean_text = InputValidator.sanitize_text(text)
```

---

### 2. Rate Limiting

#### Rate Limit Configuration:
- **Per Minute:** 10 requests
- **Per Hour:** 100 requests
- **Cooldown:** 2 seconds between requests

#### Purpose:
- Prevent abuse and DoS attacks
- Ensure fair resource allocation
- Protect against automated scraping
- Maintain application performance

#### User Feedback:
- Real-time rate limit status in sidebar
- Clear error messages when limits exceeded
- Countdown timer for cooldown period

---

### 3. XSS (Cross-Site Scripting) Protection

#### Measures:
- All HTML/Script tags removed from input
- User input never executed as code
- Output properly escaped
- `unsafe_allow_html` used only for trusted static content

#### Blocked Patterns:
```
<script>...</script>
<iframe>...</iframe>
<object>...</object>
<embed>...</embed>
```

---

### 4. SQL Injection Prevention

#### Detection:
- Pattern matching for SQL keywords
- Blocked keywords: SELECT, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, EXEC

#### Note:
While this application doesn't use a database, SQL injection prevention is implemented as a security best practice for future extensibility.

---

### 5. Spam Detection

#### Spam Indicators:
- Excessive promotional keywords (viagra, lottery, winner)
- Multiple exclamation marks (!!!!!!)
- Excessive dollar signs ($$$)
- Too many URLs (5+ links)

#### Action:
Spam content is rejected with a clear error message.

---

### 6. Session Management

#### Features:
- Unique session ID per user
- 60-minute session timeout
- Automatic session refresh on activity
- Session-isolated data storage

#### Implementation:
```python
from utils.security import SessionManager

# Initialize session
SessionManager.initialize_session()

# Check validity
if SessionManager.check_session_validity():
    # Session is valid
    SessionManager.refresh_session()
```

---

### 7. Security Logging

#### Logged Events:
- Validation errors
- Rate limit violations
- Spam detection
- Analysis success/failure
- Security incidents

#### Log Storage:
- In-memory only (session state)
- Maximum 100 logs retained
- Cleared on session end
- No persistent storage

---

## 🔐 Privacy Policy

### Data Collection

**WE DO NOT COLLECT, STORE, OR TRANSMIT ANY USER DATA**

#### What We DON'T Do:
- ❌ No database storage
- ❌ No server-side logging
- ❌ No analytics tracking
- ❌ No cookies (except Streamlit default)
- ❌ No third-party API calls
- ❌ No personal information collection
- ❌ No IP address logging
- ❌ No user profiling

#### What We DO:
- ✅ Process text locally in your browser session
- ✅ Store analysis history in session state only
- ✅ Clear all data when you close the app
- ✅ Keep rate limit counters in session state
- ✅ Maintain security logs in-memory only

### Data Lifecycle

1. **Input:** User enters text
2. **Processing:** Text analyzed in current session
3. **Display:** Results shown to user
4. **Storage:** Temporarily stored in session state
5. **Deletion:** Automatically cleared on session end

### Session Data

Only stored in browser session state:
- Analysis history (last 10)
- Rate limit counters
- Session statistics
- Security logs (last 100)

**All data is ephemeral and never leaves your browser.**

---

## 🔍 Security Best Practices for Users

### 1. Input Safety
- Don't enter sensitive information (passwords, API keys, personal data)
- Avoid pasting untrusted content
- Be cautious with very long text

### 2. Rate Limits
- Respect rate limits (10/min, 100/hour)
- Wait for cooldown periods
- Don't attempt to circumvent limits

### 3. Responsible Use
- Use for legitimate sentiment analysis only
- Don't attempt to exploit vulnerabilities
- Report security issues responsibly

### 4. Browser Security
- Use updated browser
- Enable JavaScript (required for Streamlit)
- Clear browser cache periodically

---

## 🚨 Security Incident Response

### Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** publicly disclose the issue
2. Email: [ishanrock1234@gmail.com](mailto:ishanrock1234@gmail.com)
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **24 hours:** Initial acknowledgment
- **72 hours:** Preliminary assessment
- **7 days:** Fix implementation (for critical issues)
- **14 days:** Public disclosure (after fix)

---

## 🔧 Security Configuration

### For Developers

#### Adjusting Rate Limits

Edit `utils/security.py`:

```python
class RateLimiter:
    MAX_REQUESTS_PER_MINUTE = 10  # Adjust as needed
    MAX_REQUESTS_PER_HOUR = 100    # Adjust as needed
    COOLDOWN_SECONDS = 2            # Adjust as needed
```

#### Adjusting Input Limits

```python
class InputValidator:
    MAX_TEXT_LENGTH = 10000  # Maximum characters
    MAX_WORD_COUNT = 2000     # Maximum words
```

#### Disabling Security Features (NOT RECOMMENDED)

To disable specific features, comment out relevant checks in `ui/home.py`.

**WARNING:** Disabling security features may expose the application to abuse.

---

## 📊 Security Audit Log

### Version 1.0.0 (January 2026)

#### Implemented:
- ✅ Input validation
- ✅ Rate limiting
- ✅ XSS protection
- ✅ SQL injection prevention
- ✅ Spam detection
- ✅ Session management
- ✅ Security logging

#### Tested:
- ✅ XSS payloads
- ✅ SQL injection attempts
- ✅ Rate limit enforcement
- ✅ Input validation edge cases
- ✅ Session timeout behavior

#### Known Limitations:
- Rate limits are session-based (can be bypassed with new sessions)
- Advanced evasion techniques not detected
- No CAPTCHA implementation

---

## 🎯 Future Security Enhancements

### Planned (v2.0):
- [ ] CAPTCHA integration
- [ ] IP-based rate limiting
- [ ] Advanced spam detection (ML-based)
- [ ] Content Security Policy headers
- [ ] Security headers (HSTS, X-Frame-Options)
- [ ] API key authentication (for future API)

### Under Consideration:
- [ ] Two-factor authentication (for user accounts)
- [ ] Encrypted data storage (for persistent history)
- [ ] Audit trail export
- [ ] Admin dashboard for monitoring

---

## 📜 Compliance

### Standards Followed:
- **OWASP Top 10** - Web application security
- **GDPR** - No personal data collection (by design)
- **CCPA** - Privacy by default
- **SOC 2** - Security best practices

### Certifications:
- None currently (open-source project)
- Available for commercial licensing with audit

---

## 🔐 Encryption

### Data in Transit:
- Uses HTTPS when deployed (Streamlit Cloud default)
- No sensitive data transmitted

### Data at Rest:
- No persistent storage
- Session data in-memory only (browser-side)

---

## 🛡️ Security Checklist for Deployment

Before deploying:

- [x] All security features enabled
- [x] Rate limits configured
- [x] Input validation active
- [x] XSS protection enabled
- [x] SQL injection prevention active
- [x] Spam detection working
- [x] Session management implemented
- [x] Security logging functional
- [ ] HTTPS enabled (via Streamlit Cloud)
- [ ] Domain secured
- [ ] CSP headers configured (optional)
- [ ] Security headers set (optional)

---

## 📞 Contact & Support

### Security Contact:
- **Email:** [ishanrock1234@gmail.com](mailto:ishanrock1234@gmail.com)
- **GitHub:** [@Ishan96Dev](https://github.com/Ishan96Dev)

### General Support:
- **Issues:** [GitHub Issues](https://github.com/Ishan96Dev/SentimentScope-NLP-Sentiment-Analysis-App/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Ishan96Dev/SentimentScope-NLP-Sentiment-Analysis-App/discussions)

---

## ⚖️ Legal

### Disclaimer

This software is provided "as is" without warranty of any kind. The author is not responsible for:
- Data loss or corruption
- Security breaches from misconfiguration
- Third-party modifications
- Misuse of the application

### License

MIT License - See [LICENSE](LICENSE) file for details.

### Copyright

© 2026 Ishan Chakraborty. All rights reserved.

---

**Last Updated:** January 19, 2026  
**Version:** 1.0.0  
**Author:** Ishan Chakraborty
