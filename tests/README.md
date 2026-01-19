# Tests Directory

## 🧪 Testing Structure

This directory will contain all test files for the SentimentScope application.

## Planned Test Files

```
tests/
├── __init__.py
├── test_analyzer.py        # Sentiment analyzer tests
├── test_security.py        # Security validation tests
├── test_ui.py             # UI component tests
└── test_integration.py    # Integration tests
```

## Running Tests

### Using pytest

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=sentiment --cov=utils --cov=ui tests/

# Run specific test file
pytest tests/test_analyzer.py

# Run with verbose output
pytest -v tests/
```

## Test Categories

### 1. Unit Tests
- Test individual functions in isolation
- Mock external dependencies
- Fast execution

### 2. Integration Tests
- Test module interactions
- Test full analysis pipeline
- Test UI rendering

### 3. Security Tests
- Test input validation
- Test XSS prevention
- Test SQL injection blocking
- Test rate limiting

### 4. Performance Tests
- Test analysis speed
- Test memory usage
- Test concurrent requests

## Example Test Structure

```python
# tests/test_analyzer.py
import pytest
from sentiment.analyzer import SentimentAnalyzer

def test_positive_sentiment():
    """Test positive sentiment detection"""
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze("I love this product!")
    
    assert result['label'] == 'Positive'
    assert result['polarity'] > 0
    assert result['confidence'] > 0

def test_negative_sentiment():
    """Test negative sentiment detection"""
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze("This is terrible!")
    
    assert result['label'] == 'Negative'
    assert result['polarity'] < 0

def test_empty_input():
    """Test error handling for empty input"""
    analyzer = SentimentAnalyzer()
    
    with pytest.raises(ValueError):
        analyzer.analyze("")
```

## Test Coverage Goals

- **Unit Tests:** > 80% code coverage
- **Integration Tests:** All critical paths
- **Security Tests:** All validation rules
- **Performance Tests:** Key bottlenecks

## Contributing Tests

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain > 80% coverage
4. Document test cases

---

**Status:** Tests to be implemented  
**Priority:** High  
**Framework:** pytest
