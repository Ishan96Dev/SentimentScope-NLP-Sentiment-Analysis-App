"""
API Integration Module

Provides RESTful API endpoints for sentiment analysis, enabling external applications
to integrate with SentimentScope programmatically.

Features:
- FastAPI-based REST endpoints
- JWT authentication (optional)
- Rate limiting per API key
- Batch processing support
- Real-time analysis
- Historical data retrieval

Author: Ishan Chakraborty
License: MIT
"""

__all__ = ["api_server", "api_client"]
