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
        Clean and sanitize input text for safe sentiment analysis.
        
        Performs HTML entity decoding, collapses repeated whitespace, removes potentially unsafe characters while preserving common punctuation, and reduces excessive repeated characters to mitigate spam.
        
        Parameters:
            text (str): Raw input text to be cleaned.
        
        Returns:
            str: The cleaned and sanitized text.
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
        Analyze input text and return a structured sentiment analysis result.
        
        Parameters:
            text (str): Text to analyze. Must be non-empty, at most 10,000 characters, and contain at most 2,000 words.
        
        Returns:
            result (dict): Mapping with sentiment analysis details:
                - label (str): "Positive", "Neutral", or "Negative".
                - confidence (float): Confidence score in range 0–100.
                - polarity (float): Sentiment polarity rounded to 3 decimals (-1.0 to 1.0).
                - subjectivity (float): Subjectivity score rounded to 3 decimals (0.0 to 1.0).
                - emoji (str): Representative emoji for the sentiment.
                - color (str): Hex color code associated with the sentiment.
                - text_length (int): Number of characters in the original input.
                - word_count (int): Number of words in the original input.
                - word_sentiments (list): List of per-word sentiment dicts (word, polarity, sentiment, impact).
                - sentiment_keywords (dict): Top positive and negative keyword lists and their totals.
                - emotions (dict): Detected emotions profile including primary emotion, scores, confidence, and top emotions.
                - advanced_keywords (dict): Extracted noun phrases, frequent words, and combined keyword metadata.
        
        Raises:
            ValueError: If input is empty after trimming/preprocessing, exceeds allowed character or word limits.
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
        Map a polarity score to a sentiment label, emoji, and color.
        
        Parameters:
            polarity (float): Polarity score (typically -1.0 to 1.0) used to determine sentiment.
        
        Returns:
            tuple: (label, emoji, color_hex) where
                - label (str): "Positive", "Negative", or "Neutral" determined by class thresholds
                - emoji (str): single-character emoji representing the sentiment
                - color_hex (str): hex color code associated with the sentiment
        """
        if polarity >= self.POSITIVE_THRESHOLD:
            return "Positive", "😊", "#10b981"  # Green
        elif polarity <= self.NEGATIVE_THRESHOLD:
            return "Negative", "😠", "#ef4444"  # Red
        else:
            return "Neutral", "😐", "#f59e0b"   # Yellow/Orange
    
    def _calculate_confidence(self, polarity: float, subjectivity: float) -> float:
        """
        Compute a confidence score (0–100) for a sentiment result based on polarity and subjectivity.
        
        Parameters:
            polarity (float): Sentiment polarity in the range -1 to 1; larger absolute values indicate stronger sentiment.
            subjectivity (float): Subjectivity in the range 0 to 1; higher values indicate more subjective (opinionated) text.
        
        Returns:
            float: Confidence value between 0 and 100, rounded to two decimals.
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
        Analyze per-word sentiment contributions from a TextBlob.
        
        Processes each word in the provided TextBlob and returns influential words with their polarity, categorical sentiment, and impact score, sorted by impact descending.
        
        Parameters:
            blob (TextBlob): TextBlob instance created from the source text to analyze.
        
        Returns:
            List[Dict]: A list of dictionaries (possibly empty). Each dictionary contains:
                - "word" (str): Lowercased word text.
                - "polarity" (float): Sentiment polarity rounded to 3 decimals (negative to positive).
                - "sentiment" (str): One of "Positive", "Negative", or "Neutral".
                - "impact" (float): Absolute value of the polarity, used to rank influence.
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
        Classify a single word polarity as "Positive", "Negative", or "Neutral".
        
        Parameters:
            polarity (float): Polarity score for the word; positive values indicate positive sentiment, negative values indicate negative sentiment, zero indicates neutral.
        
        Returns:
            str: One of "Positive", "Negative", or "Neutral" corresponding to the polarity.
        """
        if polarity > 0:
            return "Positive"
        elif polarity < 0:
            return "Negative"
        else:
            return "Neutral"
    
    def _extract_sentiment_keywords(self, word_sentiments: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Retrieve the top positive and negative sentiment keywords from word-level sentiment data.
        
        Filters the provided word sentiment entries by their "sentiment" field and returns up to five positive and five negative entries along with counts.
        
        Parameters:
            word_sentiments (List[Dict]): List of word sentiment dictionaries; each dictionary is expected to contain at least the keys `"word"` and `"sentiment"`.
        
        Returns:
            Dict[str, List[Dict]]: Dictionary with the following keys:
                - "positive": list of up to five word sentiment dicts whose `"sentiment"` is "Positive"
                - "negative": list of up to five word sentiment dicts whose `"sentiment"` is "Negative"
                - "total_positive": integer count of positive words found
                - "total_negative": integer count of negative words found
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
        Detect the predominant emotion and produce normalized emotion scores based on keyword signals and sentiment metrics.
        
        Analyzes the lowercase text for presence of emotion-related keywords, adjusts raw emotion scores using polarity and subjectivity, normalizes scores to a 0–100 scale, and returns a structured emotion profile.
        
        Parameters:
            text (str): Original input text.
            blob (TextBlob): TextBlob instance for optional linguistic features (not required by this implementation).
            polarity (float): Sentiment polarity in the range -1.0 to 1.0; used to boost positive or negative emotion scores.
            subjectivity (float): Subjectivity in the range 0.0 to 1.0; used to boost emotions when text is more subjective.
        
        Returns:
            dict: Emotion analysis with keys:
                - "primary_emotion" (str): Capitalized name of the highest-scoring emotion.
                - "emotion_scores" (Dict[str, float]): Normalized scores for each emotion on a 0–100 scale.
                - "confidence" (float): Score of the primary emotion (0–100).
                - "top_emotions" (List[Dict]): Up to three top emotions as {"emotion": name, "score": value}.
                - "emotion_detected" (bool): True if the primary emotion's confidence is greater than 20, False otherwise.
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
        Extracts salient keywords from a TextBlob using noun phrase and word frequency analysis.
        
        Parameters:
            blob (TextBlob): Parsed text object providing noun_phrases and words.
            word_sentiments (List[Dict]): List of word-level sentiment dictionaries (each must contain a `"word"` key), ordered by impact.
        
        Returns:
            Dict[str, Any]: A dictionary with:
                - "noun_phrases" (List[str]): Up to 5 most frequent noun phrases.
                - "frequent_words" (List[str]): Up to 10 most frequent words longer than 3 characters.
                - "sentiment_keywords" (List[str]): Up to 10 top words extracted from `word_sentiments`.
                - "total_keywords" (int): Count of unique keywords across `frequent_words` and `sentiment_keywords`.
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
        Analyze a list of texts and return per-text analysis results.
        
        Parameters:
            texts (list): List of input text strings to analyze.
        
        Returns:
            list: A list where each element is either:
                - an analysis dictionary produced by analyze(...) with an added
                  "original_text" key containing the input text, or
                - an error dictionary with keys "original_text" and "error" when
                  analysis failed for that input.
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