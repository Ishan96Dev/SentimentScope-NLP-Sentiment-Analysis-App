# 🧠 SentimentScope - NLP Sentiment Analysis App

**Author:** Ishan Chakraborty  
**License:** MIT  
**Copyright:** © 2026

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-TextBlob-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

A professional, production-ready **Streamlit web application** for real-time sentiment analysis using Natural Language Processing (NLP). Detect sentiment (Positive, Neutral, Negative) with confidence scores and beautiful visualizations.

🌐 **[Try the Live App](https://sentimentscope-nlp-sentiment-analysis-app.streamlit.app/)** 🚀

---

## ✨ Features

### 🎯 Core Functionality
- **Real-time Sentiment Analysis** - Instant sentiment detection as you type
- **Confidence Scoring** - See how confident the model is about its prediction
- **Visual Polarity Gauge** - Interactive gauge chart showing sentiment strength
- **Multiple Sentiment Types** - Positive 😊, Neutral 😐, Negative 😠

### 🛡️ Security Features
- **Input Validation** - Comprehensive validation and sanitization
- **Rate Limiting** - 10 requests/minute, 100/hour
- **XSS Protection** - HTML/Script tag filtering
- **SQL Injection Prevention** - Pattern-based detection
- **Spam Detection** - Automated spam filtering
- **Session Management** - Secure session handling
- **Length Limits** - Maximum 10k characters, 2k words

### 🎨 User Experience
- **Clean, Modern UI** - Professional design with intuitive navigation
- **Quick Examples** - One-click example sentences for testing
- **Analysis History** - Track your recent analyses
- **Export Results** - Download analysis reports as text files
- **Real-time Stats** - Character and word counters
- **Responsive Design** - Works seamlessly on desktop and mobile

### 📊 Analytics
- **Detailed Metrics** - Polarity, subjectivity, confidence scores
- **Visual Representations** - Interactive charts and progress bars
- **Interpretation Guide** - Understand what the results mean
- **Session Statistics** - Track total analyses performed

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Streamlit-Sentiment-Analysis-App
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data (first time only)**
   ```python
   python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   - The app will automatically open at `http://localhost:8501`

---

## 📁 Project Structure

```
Streamlit-Sentiment-Analysis-App/
│
├── app.py                      # Main application entry point
│
├── sentiment/                  # Sentiment analysis module
│   ├── __init__.py
│   └── analyzer.py            # Core sentiment analysis logic
│
├── ui/                        # UI components
│   ├── __init__.py
│   ├── home.py               # Main analyzer screen
│   └── about.py              # About/info screen
│
├── assets/                    # Static assets (logos, images)
│
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── config.py                # Configuration settings
```

---

## 🎮 How to Use

### Basic Usage

1. **Navigate to Sentiment Analyzer**
   - The main screen opens by default
   - Or click "Sentiment Analyzer" in the sidebar

2. **Enter Your Text**
   - Type or paste text into the text area
   - Or click a "Quick Example" button to test

3. **Click "Analyze Sentiment"**
   - Results appear instantly below

4. **View Results**
   - Sentiment label (Positive/Neutral/Negative)
   - Confidence percentage
   - Visual polarity gauge
   - Detailed metrics

5. **Export Results (Optional)**
   - Click "Download Report" to save analysis

### Navigation

- **🧠 Sentiment Analyzer** - Main analysis screen
- **ℹ️ About App** - Learn about sentiment analysis and features

---

## 🔬 Technical Details

### NLP Model

**SentimentScope** uses **TextBlob**, a Python library for processing textual data:

- **Polarity Score**: -1 (most negative) to +1 (most positive)
- **Subjectivity Score**: 0 (objective) to 1 (subjective)
- **Classification Thresholds**:
  - Positive: Polarity ≥ 0.1
  - Neutral: -0.1 < Polarity < 0.1
  - Negative: Polarity ≤ -0.1

### Confidence Calculation

Confidence is calculated using:
```
confidence = abs(polarity) * 100 * (0.3 + subjectivity * 0.7)
```

Higher subjectivity indicates clearer sentiment, resulting in higher confidence.

### Features Explained

| Feature | Description |
|---------|-------------|
| **Polarity** | Sentiment direction (-1 to +1) |
| **Subjectivity** | Opinion vs fact (0 to 1) |
| **Confidence** | Model certainty (0% to 100%) |
| **Label** | Classification result |

---

## 📊 Example Results

### Positive Sentiment
```
Text: "I absolutely loved the experience! It was amazing."
Sentiment: Positive 😊
Confidence: 94.2%
Polarity: 0.742
```

### Neutral Sentiment
```
Text: "The product arrived on time and works as described."
Sentiment: Neutral 😐
Confidence: 38.5%
Polarity: 0.042
```

### Negative Sentiment
```
Text: "This is the worst service I've ever experienced."
Sentiment: Negative 😠
Confidence: 97.8%
Polarity: -0.921
```

---

## 🎯 Use Cases

- **Customer Feedback Analysis** - Understand customer satisfaction
- **Social Media Monitoring** - Track brand sentiment on platforms
- **Product Review Analysis** - Aggregate user opinions
- **Email Classification** - Prioritize urgent or negative messages
- **Content Moderation** - Detect toxic or negative content
- **Survey Analysis** - Process open-ended responses
- **Market Research** - Analyze consumer sentiment

---

## ⚙️ Configuration

### Environment Variables (Optional)

Create a `.env` file for custom configurations:

```env
# App Configuration
APP_TITLE="SentimentScope"
APP_ICON="🧠"

# Model Settings
POSITIVE_THRESHOLD=0.1
NEGATIVE_THRESHOLD=-0.1

# UI Settings
MAX_HISTORY_ITEMS=10
```

### Custom Thresholds

Edit `sentiment/analyzer.py` to adjust classification thresholds:

```python
class SentimentAnalyzer:
    POSITIVE_THRESHOLD = 0.1   # Adjust as needed
    NEGATIVE_THRESHOLD = -0.1  # Adjust as needed
```

---

## 🚧 Roadmap & Future Features

### Version 2.0 (Planned)
- [ ] Batch CSV file analysis
- [ ] Multi-language support
- [ ] Advanced emotion detection (joy, anger, fear, etc.)
- [ ] Aspect-based sentiment analysis
- [ ] Keyword and entity extraction

### Version 3.0 (Future)
- [ ] Transformer-based models (BERT, RoBERTa)
- [ ] API endpoints for integration
- [ ] User authentication and accounts
- [ ] Persistent analysis history
- [ ] Team collaboration features
- [ ] Custom model training interface

---

## 🐛 Known Limitations

1. **Language**: Optimized for English text only
2. **Sarcasm**: May not detect sarcasm or irony accurately
3. **Context**: Limited understanding of complex context
4. **Short Text**: Less accurate on very short texts (< 5 words)
5. **Domain**: General-purpose; may need fine-tuning for specialized domains

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black .

# Lint code
flake8 .
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright © 2026 Ishan Chakraborty**

---

## 👨‍💻 Author

**Ishan Chakraborty**

- GitHub: [@Ishan96Dev](https://github.com/Ishan96Dev)
- Email: [ishanrock1234@gmail.com](mailto:ishanrock1234@gmail.com)

---

## 🙏 Acknowledgments

- **Streamlit** - Amazing framework for data apps
- **TextBlob** - Simple and powerful NLP library
- **Plotly** - Interactive visualization library
- **Open Source Community** - For inspiration and support

---

## 📧 Contact & Support

- **GitHub**: [Ishan96Dev](https://github.com/Ishan96Dev)
- **Email**: [ishanrock1234@gmail.com](mailto:ishanrock1234@gmail.com)
- **Documentation**: [Overview](docs/overview.md)

---

## ⭐ Show Your Support

If you find this project helpful, please give it a ⭐ on GitHub!

---

**Built with ❤️ by Ishan Chakraborty using Streamlit and Natural Language Processing**

**© 2026 Ishan Chakraborty | MIT License**

*Last Updated: January 2026*
