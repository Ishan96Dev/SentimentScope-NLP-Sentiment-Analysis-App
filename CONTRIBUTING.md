# Contributing to SentimentScope

Thank you for considering contributing to SentimentScope! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of NLP and Streamlit

### Development Setup

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/Streamlit-Sentiment-Analysis-App.git
   cd Streamlit-Sentiment-Analysis-App
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Unix/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   python -m textblob.download_corpora
   ```

4. **Create a branch for your feature**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Making Changes

### Project Structure

Refer to [STRUCTURE.md](STRUCTURE.md) for the project organization.

### Key Modules

- **sentiment/analyzer.py**: Core NLP logic
- **ui/home.py**: Main user interface
- **ui/about.py**: Information page
- **utils/security.py**: Security and validation

### Before You Start

1. Check existing issues to avoid duplicates
2. Create an issue describing your proposed change
3. Wait for feedback before starting major work

## 📝 Coding Standards

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) conventions:

```python
# Good
def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of input text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with sentiment results
    """
    # Implementation
    pass

# Bad
def analyzeSentiment(text):
    # No docstring
    pass
```

### Code Quality Checklist

- [ ] Code follows PEP 8 style guide
- [ ] All functions have docstrings
- [ ] Type hints are used where appropriate
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] Error handling is implemented
- [ ] Security best practices followed

## 🧪 Testing Guidelines

### Writing Tests

```python
# tests/test_analyzer.py
import pytest
from sentiment.analyzer import SentimentAnalyzer

def test_positive_sentiment():
    """Test positive sentiment detection"""
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze("I love this!")
    
    assert result['label'] == 'Positive'
    assert result['confidence'] > 0
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test
pytest tests/test_analyzer.py::test_positive_sentiment
```

### Test Coverage

- Aim for > 80% code coverage
- Test happy paths and edge cases
- Include security tests for validation
- Test error handling

## 📤 Submitting Changes

### Pull Request Process

1. **Update documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update STRUCTURE.md for new files

2. **Ensure tests pass**
   ```bash
   pytest tests/
   ```

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add feature description"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

### Commit Message Format

Use conventional commits format:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic change)
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Build process or auxiliary tools

**Examples:**
```
feat: Add multi-language sentiment analysis

Add support for Spanish and French languages using 
multilingual TextBlob models.

Closes #123
```

```
fix: Resolve rate limiting bug

Fixed issue where rate limiter wasn't resetting properly
after timeout period.

Fixes #456
```

## 📚 Documentation

### Updating Documentation

When adding features, update:

1. **README.md**: User-facing features
2. **docs/DOCUMENTATION.md**: API reference
3. **docs/QUICK_REFERENCE.md**: Developer shortcuts
4. **Docstrings**: Inline code documentation

### Documentation Style

```python
def analyze_sentiment(text: str, language: str = "en") -> dict:
    """
    Analyze sentiment of text in specified language.
    
    This function processes text through multiple stages:
    1. Validation and sanitization
    2. Language detection (if not specified)
    3. NLP analysis using TextBlob
    4. Classification and confidence scoring
    
    Args:
        text (str): Input text to analyze (1-10,000 characters)
        language (str, optional): Language code (default: "en")
            Supported: "en", "es", "fr"
            
    Returns:
        dict: Analysis results containing:
            - label (str): "Positive", "Neutral", or "Negative"
            - confidence (float): Confidence score (0-100%)
            - polarity (float): Polarity score (-1.0 to +1.0)
            - subjectivity (float): Subjectivity score (0.0 to 1.0)
            
    Raises:
        ValueError: If text is empty or too long
        LanguageNotSupportedError: If language is not supported
        
    Example:
        >>> analyzer = SentimentAnalyzer()
        >>> result = analyzer.analyze("I love this!")
        >>> print(result['label'])
        'Positive'
    """
    pass
```

## 🐛 Reporting Bugs

### Bug Report Template

When reporting bugs, include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Numbered steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, Python version, dependency versions
6. **Screenshots**: If applicable
7. **Logs**: Error messages or stack traces

## 💡 Feature Requests

### Feature Request Template

When requesting features, include:

1. **Problem**: What problem does this solve?
2. **Proposed Solution**: How would you implement it?
3. **Alternatives**: Other solutions you considered
4. **Additional Context**: Screenshots, mockups, examples

## 📞 Getting Help

- **Issues**: Open an issue on GitHub
- **Email**: ishanrock1234@gmail.com
- **Discussions**: Use GitHub Discussions for questions

## 🎯 Priority Areas

We especially welcome contributions in:

- [ ] Multi-language support
- [ ] Batch CSV analysis
- [ ] Emotion detection
- [ ] API endpoints
- [ ] Unit tests
- [ ] Performance optimization
- [ ] UI improvements
- [ ] Documentation enhancements

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to SentimentScope!** 🙏

**Author:** Ishan Chakraborty  
**Email:** ishanrock1234@gmail.com  
**GitHub:** [@Ishan96Dev](https://github.com/Ishan96Dev)
