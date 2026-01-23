"""
Sentiment Analysis Module
==========================
Core NLP sentiment analysis functionality for SentimentScope

PURPOSE:
    This package contains the sentiment analysis engine that processes text
    and determines emotional tone (positive, neutral, negative) along with
    word-level sentiment impact analysis.

MAIN COMPONENTS:
    - analyzer.py: SentimentAnalyzer class with analysis methods
    - Word-level sentiment scoring and keyword extraction
    - Confidence calculation and polarity determination

KEY FEATURES:
    ✅ Overall sentiment classification
    ✅ Polarity scoring (-1 to +1 scale)
    ✅ Subjectivity measurement
    ✅ Confidence calculation
    ✅ Word-level sentiment impact
    ✅ Top keyword identification
    ✅ Batch analysis support

USAGE:
    ```python
    from sentiment.analyzer import get_analyzer
    
    analyzer = get_analyzer()
    result = analyzer.analyze("I love this product!")
    
    print(result['label'])           # "Positive"
    print(result['confidence'])      # 85.5
    print(result['word_sentiments']) # [{"word": "love", ...}]
    ```

COMPLEXITY:
    - Single analysis: O(n+m) where n=chars, m=words
    - Batch analysis: O(k×(n+m)) where k=number of texts

Author: Ishan Chakraborty
License: MIT
"""

from sentiment.analyzer import get_analyzer, SentimentAnalyzer

__all__ = ['get_analyzer', 'SentimentAnalyzer']
