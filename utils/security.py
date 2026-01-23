"""
Security and Validation Utilities for SentimentScope
=====================================================
Comprehensive security module providing input validation, rate limiting,
security logging, and session management.

This module implements multiple layers of security protection:

1. INPUT VALIDATION (InputValidator class):
   - Text length limits (1-10,000 characters, max 2,000 words)
   - XSS (Cross-Site Scripting) prevention
   - SQL injection pattern detection
   - HTML tag removal and sanitization
   - Spam content detection
   - Special character ratio validation

2. RATE LIMITING (RateLimiter class):
   - Per-minute limits (10 requests max)
   - Per-hour limits (100 requests max)
   - Cooldown period (2 seconds between requests)
   - Usage statistics tracking
   - Session-based request counting

3. SECURITY LOGGING (SecurityLogger class):
   - Event logging (validation errors, rate limits, analysis success/failure)
   - In-memory log storage (last 100 entries)
   - Timestamp tracking for all events
   - Event type categorization

4. SESSION MANAGEMENT (SessionManager class):
   - Secure session initialization
   - Session timeout (60 minutes)
   - Session validity checking
   - Automatic session refresh
   - Unique session ID generation

Security Principles:
- Defense in depth: Multiple validation layers
- Fail-safe defaults: Reject invalid input by default
- Minimal attack surface: Strict input filtering
- Audit trail: All security events logged
- Resource limits: Prevent DoS attacks

Author: Ishan Chakraborty
Email: ishanrock1234@gmail.com
GitHub: @Ishan96Dev
License: MIT
"""

# ============================================================================
# IMPORTS
# ============================================================================

import re  # Regular expressions for pattern matching and validation
import time  # Time tracking for rate limiting and cooldowns
from typing import Optional, Tuple  # Type hints for better code documentation
from datetime import datetime, timedelta  # Date/time handling for sessions and logging
import streamlit as st  # Streamlit session state for data persistence


class InputValidator:
    """
    Validates and sanitizes user input for security
    """
    
    # Security limits
    MIN_TEXT_LENGTH = 1
    MAX_TEXT_LENGTH = 10000  # 10k characters max
    MAX_WORD_COUNT = 2000
    
    # Patterns for malicious content detection
    SCRIPT_PATTERN = re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL)
    HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
    SQL_INJECTION_PATTERN = re.compile(
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)",
        re.IGNORECASE
    )
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Remove script and HTML tags, truncate to MAX_TEXT_LENGTH, and strip surrounding whitespace.
        
        If the input is falsy, returns an empty string. The returned string has script tags and other HTML tags removed, is limited to InputValidator.MAX_TEXT_LENGTH characters, and has leading/trailing whitespace trimmed.
        
        Returns:
            Sanitized text with script and HTML tags removed, truncated to MAX_TEXT_LENGTH, and stripped of leading/trailing whitespace.
        """
        if not text:
            return ""
        
        # Remove script tags
        text = InputValidator.SCRIPT_PATTERN.sub('', text)
        
        # Remove HTML tags
        text = InputValidator.HTML_TAG_PATTERN.sub('', text)
        
        # Limit length
        text = text[:InputValidator.MAX_TEXT_LENGTH]
        
        return text.strip()
    
    @staticmethod
    def validate_input(text: str) -> Tuple[bool, Optional[str]]:
        """
        Validate and enforce security and content constraints on a user-provided text string.
        
        Performs fail-fast checks for empty or whitespace-only input, minimum and maximum character limits, maximum word count, presence of SQL keywords, and excessive special-character ratio.
        
        Parameters:
            text (str): The input text to validate.
        
        Returns:
            tuple: `(True, None)` if the text passes all checks, otherwise `(False, error_message)` where `error_message` explains the first violated constraint.
        """
        if not text or not text.strip():
            return False, "⚠️ Please enter some text to analyze."
        
        # Check minimum length
        if len(text.strip()) < InputValidator.MIN_TEXT_LENGTH:
            return False, "⚠️ Text is too short. Please enter at least 1 character."
        
        # Check maximum length
        if len(text) > InputValidator.MAX_TEXT_LENGTH:
            return False, f"⚠️ Text is too long. Maximum {InputValidator.MAX_TEXT_LENGTH} characters allowed."
        
        # Check word count
        word_count = len(text.split())
        if word_count > InputValidator.MAX_WORD_COUNT:
            return False, f"⚠️ Too many words. Maximum {InputValidator.MAX_WORD_COUNT} words allowed."
        
        # Check for potential SQL injection
        if InputValidator.SQL_INJECTION_PATTERN.search(text):
            return False, "⚠️ Invalid input detected. Please remove SQL keywords."
        
        # Check for excessive special characters (potential attack)
        special_char_ratio = len(re.findall(r'[^a-zA-Z0-9\s\.\,\!\?\-\']', text)) / max(len(text), 1)
        if special_char_ratio > 0.5:
            return False, "⚠️ Text contains too many special characters."
        
        return True, None
    
    @staticmethod
    def is_spam(text: str) -> bool:
        """
        Detects whether the given text matches common spam indicators.
        
        Checks for spam keywords (e.g., promotional or scam terms), repeated special-character patterns (e.g., multiple dollar signs or exclamation marks), and an excessive number of URLs. 
        
        Parameters:
            text (str): Input text to evaluate for spam patterns.
        
        Returns:
            bool: `True` if any spam indicator is found, `False` otherwise.
        """
        spam_indicators = [
            r'(viagra|cialis|lottery|winner|prize|click here|buy now)',
            r'(\$\$\$|!!!!!!)',
            r'(http[s]?://.*){5,}',  # Too many URLs
        ]
        
        for pattern in spam_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False


class RateLimiter:
    """
    Rate limiting to prevent abuse and ensure fair usage
    """
    
    # Rate limit settings
    MAX_REQUESTS_PER_MINUTE = 10
    MAX_REQUESTS_PER_HOUR = 100
    COOLDOWN_SECONDS = 2  # Minimum time between requests
    
    @staticmethod
    def check_rate_limit() -> Tuple[bool, Optional[str]]:
        """
        Enforces cooldown and rate limits for the current session using session state.
        
        Performs three checks: a short cooldown since the last request, a per-minute request limit, and a per-hour request limit; on success it records the current request timestamp in session state. 
        
        Returns:
            Tuple where the first element is `True` if the request is allowed and `False` otherwise; the second element is an error message string when denied, or `None` when allowed.
        """
        current_time = time.time()
        
        # Initialize rate limit tracking in session state
        if 'rate_limit_requests' not in st.session_state:
            st.session_state.rate_limit_requests = []
        
        if 'last_request_time' not in st.session_state:
            st.session_state.last_request_time = 0
        
        # Remove old requests (older than 1 hour)
        st.session_state.rate_limit_requests = [
            req_time for req_time in st.session_state.rate_limit_requests
            if current_time - req_time < 3600  # 1 hour
        ]
        
        # Check cooldown period
        time_since_last = current_time - st.session_state.last_request_time
        if time_since_last < RateLimiter.COOLDOWN_SECONDS:
            wait_time = RateLimiter.COOLDOWN_SECONDS - time_since_last
            return False, f"⏳ Please wait {wait_time:.1f} seconds before analyzing again."
        
        # Check requests per minute
        recent_requests = [
            req_time for req_time in st.session_state.rate_limit_requests
            if current_time - req_time < 60  # 1 minute
        ]
        
        if len(recent_requests) >= RateLimiter.MAX_REQUESTS_PER_MINUTE:
            return False, "⚠️ Rate limit exceeded. Please wait a minute before trying again."
        
        # Check requests per hour
        if len(st.session_state.rate_limit_requests) >= RateLimiter.MAX_REQUESTS_PER_HOUR:
            return False, "⚠️ Hourly limit reached. Please try again later."
        
        # Update tracking
        st.session_state.rate_limit_requests.append(current_time)
        st.session_state.last_request_time = current_time
        
        return True, None
    
    @staticmethod
    def get_usage_stats() -> dict:
        """
        Return current rate limit usage statistics for the active session.
        
        Returns:
            dict: Mapping with keys:
                - 'requests_last_minute' (int): number of recorded requests in the last 60 seconds.
                - 'requests_last_hour' (int): number of recorded requests in the last 3600 seconds.
                - 'remaining_minute' (int): remaining allowed requests for the minute (0 or positive).
                - 'remaining_hour' (int): remaining allowed requests for the hour (0 or positive).
        """
        if 'rate_limit_requests' not in st.session_state:
            return {
                'requests_last_minute': 0,
                'requests_last_hour': 0,
                'remaining_minute': RateLimiter.MAX_REQUESTS_PER_MINUTE,
                'remaining_hour': RateLimiter.MAX_REQUESTS_PER_HOUR
            }
        
        current_time = time.time()
        
        requests_last_minute = len([
            req for req in st.session_state.rate_limit_requests
            if current_time - req < 60
        ])
        
        requests_last_hour = len([
            req for req in st.session_state.rate_limit_requests
            if current_time - req < 3600
        ])
        
        return {
            'requests_last_minute': requests_last_minute,
            'requests_last_hour': requests_last_hour,
            'remaining_minute': max(0, RateLimiter.MAX_REQUESTS_PER_MINUTE - requests_last_minute),
            'remaining_hour': max(0, RateLimiter.MAX_REQUESTS_PER_HOUR - requests_last_hour)
        }


class SecurityLogger:
    """
    Log security events for monitoring and debugging
    """
    
    @staticmethod
    def log_event(event_type: str, details: str):
        """
        Append a timestamped security event to the in-memory session log.
        
        Stores a log entry (timestamp, type, details) in Streamlit's session_state under 'security_logs' and retains only the most recent 100 entries.
        
        Parameters:
            event_type (str): A short label for the event (e.g., "validation_error", "rate_limit").
            details (str): Human-readable details about the event.
        """
        if 'security_logs' not in st.session_state:
            st.session_state.security_logs = []
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'details': details
        }
        
        st.session_state.security_logs.append(log_entry)
        
        # Keep only last 100 logs
        if len(st.session_state.security_logs) > 100:
            st.session_state.security_logs = st.session_state.security_logs[-100:]
    
    @staticmethod
    def get_recent_logs(count: int = 10) -> list:
        """
        Return the most recent security log entries.
        
        If fewer than `count` logs exist, returns all available logs.
        
        Parameters:
            count (int): Maximum number of recent logs to retrieve.
        
        Returns:
            list: Log entries ordered chronologically (oldest to newest) limited to the `count` most recent entries; returns an empty list if no logs exist.
        """
        if 'security_logs' not in st.session_state:
            return []
        
        return st.session_state.security_logs[-count:]


class SessionManager:
    """
    Manage user sessions securely
    """
    
    SESSION_TIMEOUT_MINUTES = 60
    
    @staticmethod
    def initialize_session():
        """Initialize session with security settings"""
        if 'session_initialized' not in st.session_state:
            st.session_state.session_initialized = True
            st.session_state.session_start_time = datetime.now()
            st.session_state.session_id = f"session_{int(time.time() * 1000)}"
    
    @staticmethod
    def check_session_validity() -> bool:
        """
        Check if session is still valid
        
        Returns:
            True if session is valid
        """
        if 'session_start_time' not in st.session_state:
            return False
        
        session_age = datetime.now() - st.session_state.session_start_time
        if session_age > timedelta(minutes=SessionManager.SESSION_TIMEOUT_MINUTES):
            return False
        
        return True
    
    @staticmethod
    def refresh_session():
        """Refresh session timestamp"""
        if 'session_start_time' in st.session_state:
            st.session_state.session_start_time = datetime.now()