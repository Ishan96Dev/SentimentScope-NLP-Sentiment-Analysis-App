"""
API Client Example

Demonstrates how to use the SentimentScope API from external applications.

Usage:
    python api/api_client.py
"""

import requests
import json
from typing import Dict, List, Any


class SentimentScopeClient:
    """Client for interacting with SentimentScope API"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        """
        Create a SentimentScope API client configured with a base URL and optional API key.
        
        Parameters:
            base_url (str): Base URL of the SentimentScope API (including scheme), e.g. "http://localhost:8000".
            api_key (str | None): Optional API key; when provided it is added to headers as "X-API-Key".
        """
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["X-API-Key"] = api_key
    
    def analyze(self, text: str, include_emotions: bool = True, 
                include_keywords: bool = True) -> Dict[str, Any]:
        """
                Analyze the sentiment of a single text string.
                
                Parameters:
                    text (str): The text to analyze.
                    include_emotions (bool): If True, include detected emotions in the results.
                    include_keywords (bool): If True, include extracted keywords in the results.
                
                Returns:
                    Dict[str, Any]: Analysis result containing at least a sentiment label and confidence, and optionally detected emotions, extracted keywords, and processing metadata.
                """
        endpoint = f"{self.base_url}/api/v1/analyze"
        payload = {
            "text": text,
            "include_emotions": include_emotions,
            "include_keywords": include_keywords
        }
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def batch_analyze(self, texts: List[str], include_emotions: bool = True,
                     include_keywords: bool = True) -> Dict[str, Any]:
        """
        Analyze sentiment of multiple texts
        
        Args:
            texts: List of texts to analyze
            include_emotions: Include emotion detection results
            include_keywords: Include advanced keywords
            
        Returns:
            Batch analysis results dictionary
        """
        endpoint = f"{self.base_url}/api/v1/batch"
        payload = {
            "texts": texts,
            "include_emotions": include_emotions,
            "include_keywords": include_keywords
        }
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict[str, Any]:
        """
        Retrieve SentimentScope API health information.
        
        Returns:
            A dictionary containing health details (for example `status` and `version`).
        """
        endpoint = f"{self.base_url}/api/v1/health"
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = SentimentScopeClient()
    
    print("=" * 70)
    print("SENTIMENTSCOPE API CLIENT EXAMPLE")
    print("=" * 70)
    print()
    
    # Health check
    print("1. Health Check")
    print("-" * 70)
    health = client.health_check()
    print(f"Status: {health['status']}")
    print(f"Version: {health['version']}")
    print()
    
    # Single text analysis
    print("2. Single Text Analysis")
    print("-" * 70)
    text = "I absolutely love this product! It's amazing and exceeded all my expectations."
    result = client.analyze(text)
    
    print(f"Text: {text}")
    print(f"Sentiment: {result['data']['label']} ({result['data']['confidence']:.1f}% confident)")
    print(f"Emotion: {result['data']['emotions']['primary_emotion']}")
    print(f"Processing Time: {result['processing_time_ms']:.2f}ms")
    print()
    
    # Batch analysis
    print("3. Batch Analysis")
    print("-" * 70)
    texts = [
        "This is wonderful!",
        "I'm disappointed with the service.",
        "The product works as expected."
    ]
    
    batch_result = client.batch_analyze(texts)
    print(f"Total Processed: {batch_result['total_processed']}")
    print(f"Processing Time: {batch_result['processing_time_ms']:.2f}ms")
    print()
    
    for i, res in enumerate(batch_result['results'], 1):
        print(f"  {i}. {res['label']} - {res['emotions']['primary_emotion']}")
    
    print()
    print("=" * 70)
    print("✅ All API calls successful!")
    print("=" * 70)