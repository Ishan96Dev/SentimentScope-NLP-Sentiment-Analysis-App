"""
Utilities Module
================
Security and helper utilities for SentimentScope

PURPOSE:
    This package contains utility functions and security components
    used throughout the SentimentScope application.

MODULES:
    1. security.py - Security utilities
       - Input validation
       - Rate limiting
       - Session management
       - Security logging

USAGE:
    from utils.security import InputValidator, RateLimiter
    
    validator = InputValidator()
    if validator.validate_text(user_input):
        # Process input
        pass

Author: Ishan Chakraborty
License: MIT
"""

# Import security utilities for easier access
from utils.security import InputValidator, RateLimiter, SessionManager, SecurityLogger

__all__ = ['InputValidator', 'RateLimiter', 'SessionManager', 'SecurityLogger']
