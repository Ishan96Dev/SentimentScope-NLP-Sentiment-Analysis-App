"""
Sentiment Analysis Engine
Uses TextBlob for fast, lightweight sentiment detection

Author: Ishan Chakraborty
License: MIT
"""

from textblob import TextBlob, Word
from typing import Dict, Tuple, List, Any
import re
import html
from collections import Counter


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
        
        COMPLEXITY ANALYSIS :
        ===========================
        Time Complexity: O(n)
            - html.unescape(): O(n) - scans entire string
            - re.sub() operations: O(n) each - pattern matching on string
            - Total: O(n) where n = length of text
        
        Space Complexity: O(n)
            - Each re.sub() creates a new string: O(n)
            - String operations in Python are immutable (create new strings)
            - Temporary strings during regex operations: O(n)
        
        Data Structure Used: String (immutable character array)
        Algorithm Pattern: Sequential string processing with regex
        
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
        
        COMPLEXITY ANALYSIS :
        ===========================
        Time Complexity: O(n + m)
            - Input validation: O(1) - constant time checks
            - len(text): O(1) - Python strings cache their length
            - text.split(): O(n) - splits string into words
            - preprocess_text(): O(n) - regex operations
            - TextBlob analysis: O(m) where m = number of words/tokens
            - Dictionary construction: O(1) - fixed size dict
            - Overall: O(n + m) where n = chars, m = words
        
        Space Complexity: O(n + m)
            - cleaned_text: O(n) - copy of processed string
            - TextBlob object: O(m) - stores tokenized text
            - Result dictionary: O(1) - fixed size
            - Total: O(n + m)
        
        Data Structures Used:
            1. String - for text storage (sequential access)
            2. Dictionary (Hash Table) - for result storage (O(1) access)
        
        Algorithm Pattern: NLP Pipeline with validation gates
        
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
        
        # Extract word-level sentiment analysis
        word_sentiments = self._analyze_word_sentiments(blob)
        
        # Detect emotions
        emotions = self._detect_emotions(text, blob, polarity, subjectivity)
        
        # Extract advanced keywords
        advanced_keywords = self._extract_advanced_keywords(blob, word_sentiments)
        
        return {
            "label": label,
            "confidence": confidence,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "emoji": emoji,
            "color": color,
            "text_length": len(text),
            "word_count": len(text.split()),
            "word_sentiments": word_sentiments,
            "sentiment_keywords": self._extract_sentiment_keywords(word_sentiments),
            "emotions": emotions,  # New: emotion detection
            "advanced_keywords": advanced_keywords  # New: advanced keyword extraction
        }
    
    def _classify_sentiment(self, polarity: float) -> Tuple[str, str, str]:
        """
        Classify sentiment based on polarity score
        
        COMPLEXITY ANALYSIS :
        ===========================
        Time Complexity: O(1)
            - Float comparison: O(1) - constant time
            - If-elif-else branching: O(1) - maximum 3 comparisons
            - Return tuple creation: O(1)
        
        Space Complexity: O(1)
            - Tuple storage: O(1) - fixed 3 elements
            - No additional data structures
        
        Algorithm: Simple threshold-based classification
        Optimization: Early exit on first match (if/elif structure)
        
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
        
        COMPLEXITY ANALYSIS :
        ===========================
        Time Complexity: O(1)
            - abs(polarity): O(1) - absolute value
            - Arithmetic operations: O(1) - multiplication, addition
            - max()/min() with 2 args: O(1) - constant comparisons
            - round(): O(1)
        
        Space Complexity: O(1)
            - Float variables: O(1) - fixed memory
            - No additional data structures
        
        Algorithm: Mathematical formula evaluation
        
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
    
    def _analyze_word_sentiments(self, blob: TextBlob) -> List[Dict]:
        """
        Analyze sentiment contribution of individual words
        
        COMPLEXITY ANALYSIS (DSA):
        ===========================
        Time Complexity: O(m)
            - Iterate through m words: O(m)
            - TextBlob sentiment per word: O(1) per word (pre-computed)
            - Total: O(m) where m = number of words
        
        Space Complexity: O(m)
            - List of m word dictionaries: O(m)
            - Each dictionary: O(1) - fixed 4 keys
        
        Data Structure: List of Dictionaries
        Algorithm: Sequential word analysis with sentiment scoring
        
        Args:
            blob: TextBlob object with analyzed text
            
        Returns:
            List of dictionaries with word sentiment data
        """
        word_sentiments = []
        
        # Analyze each word's contribution
        for word in blob.words:
            # Skip very short words (articles, conjunctions, etc.)
            if len(word) <= 2:
                continue
            
            # Get word sentiment using TextBlob
            word_blob = TextBlob(str(word))
            word_polarity = word_blob.sentiment.polarity
            
            # Only include words with sentiment (non-zero polarity)
            if word_polarity != 0:
                sentiment_type = self._get_word_sentiment_type(word_polarity)
                
                word_sentiments.append({
                    "word": str(word).lower(),
                    "polarity": round(word_polarity, 3),
                    "sentiment": sentiment_type,
                    "impact": abs(word_polarity)  # Magnitude of impact
                })
        
        # Sort by impact (most influential words first)
        word_sentiments.sort(key=lambda x: x["impact"], reverse=True)
        
        return word_sentiments
    
    def _get_word_sentiment_type(self, polarity: float) -> str:
        """
        Get sentiment type for a single word
        
        COMPLEXITY ANALYSIS (DSA):
        ===========================
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            polarity: Word polarity score
            
        Returns:
            Sentiment type string
        """
        if polarity > 0:
            return "Positive"
        elif polarity < 0:
            return "Negative"
        else:
            return "Neutral"
    
    def _extract_sentiment_keywords(self, word_sentiments: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Extract top positive and negative keywords
        
        COMPLEXITY ANALYSIS (DSA):
        ===========================
        Time Complexity: O(m)
            - Filter positive words: O(m)
            - Filter negative words: O(m)
            - Slicing top 5: O(1)
            - Total: O(m) where m = number of sentiment words
        
        Space Complexity: O(k)
            - Two lists with max 5 elements each: O(k) where k ≤ 10
        
        Data Structure: Dictionary with Lists
        Algorithm: Filter and slice
        
        Args:
            word_sentiments: List of word sentiment dictionaries
            
        Returns:
            Dictionary with top positive and negative keywords
        """
        # Separate positive and negative words
        positive_words = [w for w in word_sentiments if w["sentiment"] == "Positive"]
        negative_words = [w for w in word_sentiments if w["sentiment"] == "Negative"]
        
        return {
            "positive": positive_words[:5],  # Top 5 positive words
            "negative": negative_words[:5],  # Top 5 negative words
            "total_positive": len(positive_words),
            "total_negative": len(negative_words)
        }
    
    def _detect_emotions(self, text: str, blob: TextBlob, polarity: float, subjectivity: float) -> Dict[str, Any]:
        """
        Detect emotions using keyword matching and sentiment analysis
        
        COMPLEXITY ANALYSIS (DSA):
        ===========================
        Time Complexity: O(n)
            - Convert to lowercase: O(n)
            - Keyword matching: O(k * m) where k = keywords, m = text length
            - Simplified to O(n) as k is constant
        
        Space Complexity: O(1)
            - Fixed 8 emotions dictionary: O(1)
        
        Data Structure: Dictionary for emotion scores
        Algorithm: Keyword matching + sentiment-based adjustment
        
        Args:
            text: Input text
            blob: TextBlob object
            polarity: Sentiment polarity (-1 to 1)
            subjectivity: Subjectivity score (0 to 1)
            
        Returns:
            Dictionary with emotion analysis results
        """
        text_lower = text.lower()
        
        # Emotion keyword patterns (Plutchik's wheel of emotions)
        emotion_keywords = {
            "joy": ["happy", "joy", "delight", "pleasure", "love", "amazing", "wonderful", 
                    "fantastic", "excellent", "great", "good", "glad", "cheerful", "excited"],
            "sadness": ["sad", "unhappy", "depressed", "sorrow", "grief", "miserable", 
                        "disappointed", "unfortunate", "terrible", "awful", "bad"],
            "anger": ["angry", "mad", "furious", "rage", "hate", "irritated", "annoyed", 
                      "frustrated", "outraged", "hostile"],
            "fear": ["afraid", "scared", "fear", "terrified", "anxious", "worried", 
                     "nervous", "panic", "frightened"],
            "surprise": ["surprise", "amazed", "astonished", "shocked", "unexpected", 
                         "stunned", "wow"],
            "disgust": ["disgust", "revolting", "gross", "nasty", "horrible", "repulsive"],
            "trust": ["trust", "reliable", "confident", "secure", "safe", "believe"],
            "anticipation": ["expect", "anticipate", "hope", "await", "eager", "looking forward"]
        }
        
        # Initialize emotion scores
        emotion_scores = {emotion: 0 for emotion in emotion_keywords.keys()}
        
        # Count keyword matches
        for emotion, keywords in emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    emotion_scores[emotion] += 1
        
        # Adjust scores based on sentiment polarity
        if polarity > 0.5:
            emotion_scores["joy"] += polarity * 3
            emotion_scores["trust"] += polarity * 2
        elif polarity < -0.5:
            emotion_scores["sadness"] += abs(polarity) * 2
            emotion_scores["anger"] += abs(polarity) * 2
            emotion_scores["disgust"] += abs(polarity) * 1.5
        
        # Adjust for subjectivity
        if subjectivity > 0.7:
            emotion_scores["surprise"] += subjectivity * 1.5
            emotion_scores["anticipation"] += subjectivity * 1.5
        
        # Normalize to 0-100 scale
        max_score = max(emotion_scores.values()) if max(emotion_scores.values()) > 0 else 1
        normalized_scores = {k: round((v / max_score) * 100, 1) for k, v in emotion_scores.items()}
        
        # Find primary emotion
        primary_emotion = max(normalized_scores, key=normalized_scores.get)
        confidence = normalized_scores[primary_emotion]
        
        # Get top 3 emotions
        sorted_emotions = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
        top_emotions = [{"emotion": e[0], "score": e[1]} for e in sorted_emotions[:3] if e[1] > 0]
        
        return {
            "primary_emotion": primary_emotion.capitalize(),
            "emotion_scores": normalized_scores,
            "confidence": confidence,
            "top_emotions": top_emotions,
            "emotion_detected": confidence > 20
        }
    
    def _extract_advanced_keywords(self, blob: TextBlob, word_sentiments: List[Dict]) -> Dict[str, Any]:
        """
        Extract keywords using frequency analysis and noun phrase extraction
        
        COMPLEXITY ANALYSIS (DSA):
        ===========================
        Time Complexity: O(n)
            - Noun phrase extraction: O(n)
            - Word frequency counting: O(n)
            - Sorting top words: O(k log k) where k << n
            - Total: O(n)
        
        Space Complexity: O(k)
            - Storage for unique keywords: O(k)
        
        Data Structure: Counter (hash map) for frequency
        Algorithm: Frequency analysis + noun phrase extraction
        
        Args:
            blob: TextBlob object
            word_sentiments: List of word sentiment dictionaries
            
        Returns:
            Dictionary with extracted keywords
        """
        # Extract noun phrases
        noun_phrases = list(blob.noun_phrases)
        phrase_freq = Counter(noun_phrases)
        top_phrases = [phrase for phrase, _ in phrase_freq.most_common(5)]
        
        # Get word frequencies (excluding short words)
        words = [word.lower() for word in blob.words if len(word) > 3]
        word_freq = Counter(words)
        top_words = [word for word, _ in word_freq.most_common(10)]
        
        # Sentiment keywords
        sentiment_words = [w["word"] for w in word_sentiments[:10]]
        
        return {
            "noun_phrases": top_phrases,
            "frequent_words": top_words,
            "sentiment_keywords": sentiment_words,
            "total_keywords": len(set(top_words + sentiment_words))
        }
    
    def batch_analyze(self, texts: list) -> list:
        """
        Analyze multiple texts at once
        
        COMPLEXITY ANALYSIS :
        ===========================
        Time Complexity: O(k * (n + m))
            - Iterate through k texts: O(k)
            - Each analyze() call: O(n + m) per text
            - Total: O(k * (n + m)) where k = number of texts
        
        Space Complexity: O(k * n)
            - Results list: O(k) - stores k analysis results
            - Each result dict: O(n) - contains text copies
            - Total: O(k * n)
        
        Data Structures:
            1. List (Dynamic Array) - for results collection
            2. Dictionary - for each result
        
        Algorithm: Sequential batch processing (no parallelization)
        Potential Optimization: Parallel processing for large batches
        
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
