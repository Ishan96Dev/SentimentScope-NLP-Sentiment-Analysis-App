"""
Sentiment Analysis Engine
Uses TextBlob for fast, lightweight sentiment detection

Author: Ishan Chakraborty
License: MIT
"""

from textblob import TextBlob
from typing import Dict, Tuple
import re
import html


class SentimentAnalyzer:
    """
    Analyzes sentiment of text input using TextBlob
    Returns sentiment label, confidence score, and polarity
    """
    
    # Thresholds for sentiment classification
    POSITIVE_THRESHOLD = 0.1
    NEGATIVE_THRESHOLD = -0.1
    
    def __init__(self):
        """Initialize the sentiment analyzer"""
        pass
    
    def preprocess_text(self, text: str) -> str:
        """
        Clean and preprocess input text with security measures
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned and sanitized text string
        """
        # HTML entity decode
        text = html.unescape(text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove potentially dangerous characters but keep punctuation
        # This helps prevent any injection attempts
        text = re.sub(r'[^\w\s\.\!\?\,\;\:\-\']', '', text)
        
        # Limit consecutive repeated characters (anti-spam)
        text = re.sub(r'(.)\1{4,}', r'\1\1\1', text)
        
        return text
    
    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of input text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing:
                - label: Sentiment label (Positive/Neutral/Negative)
                - confidence: Confidence score (0-100%)
                - polarity: Raw polarity score (-1 to 1)
                - subjectivity: Subjectivity score (0 to 1)
                - emoji: Corresponding emoji
                - color: Color code for UI
        """
        # Validate input
        if not text or not text.strip():
            raise ValueError("Text input cannot be empty")
        
        # Additional length validation for security
        if len(text) > 10000:
            raise ValueError("Text is too long. Maximum 10,000 characters allowed.")
        
        if len(text.split()) > 2000:
            raise ValueError("Text contains too many words. Maximum 2,000 words allowed.")
        
        # Preprocess text
        cleaned_text = self.preprocess_text(text)
        
        if not cleaned_text:
            raise ValueError("Text contains no valid content after preprocessing")
        
        # Analyze with TextBlob
        blob = TextBlob(cleaned_text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment label
        label, emoji, color = self._classify_sentiment(polarity)
        
        # Calculate confidence score (normalized to 0-100%)
        confidence = self._calculate_confidence(polarity, subjectivity)
        
        return {
            "label": label,
            "confidence": confidence,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "emoji": emoji,
            "color": color,
            "text_length": len(text),
            "word_count": len(text.split())
        }
    
    def _classify_sentiment(self, polarity: float) -> Tuple[str, str, str]:
        """
        Classify sentiment based on polarity score
        
        Args:
            polarity: Polarity score from TextBlob (-1 to 1)
            
        Returns:
            Tuple of (label, emoji, color)
        """
        if polarity >= self.POSITIVE_THRESHOLD:
            return "Positive", "😊", "#10b981"  # Green
        elif polarity <= self.NEGATIVE_THRESHOLD:
            return "Negative", "😠", "#ef4444"  # Red
        else:
            return "Neutral", "😐", "#f59e0b"   # Yellow/Orange
    
    def _calculate_confidence(self, polarity: float, subjectivity: float) -> float:
        """
        Calculate confidence score based on polarity magnitude and subjectivity
        
        Args:
            polarity: Polarity score (-1 to 1)
            subjectivity: Subjectivity score (0 to 1)
            
        Returns:
            Confidence percentage (0-100)
        """
        # Base confidence from polarity magnitude
        polarity_confidence = abs(polarity) * 100
        
        # Adjust based on subjectivity (higher subjectivity = more confident)
        # Subjective text tends to have clearer sentiment
        subjectivity_factor = 0.3 + (subjectivity * 0.7)
        
        # Combined confidence
        confidence = polarity_confidence * subjectivity_factor
        
        # Ensure confidence is between 0 and 100
        confidence = max(0, min(100, confidence))
        
        return round(confidence, 2)
    
    def batch_analyze(self, texts: list) -> list:
        """
        Analyze multiple texts at once
        
        Args:
            texts: List of text strings
            
        Returns:
            List of analysis results
        """
        results = []
        for text in texts:
            try:
                result = self.analyze(text)
                result["original_text"] = text
                results.append(result)
            except ValueError as e:
                results.append({
                    "original_text": text,
                    "error": str(e)
                })
        
        return results


# Singleton instance
_analyzer = None

def get_analyzer() -> SentimentAnalyzer:
    """Get or create singleton analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentAnalyzer()
    return _analyzer
