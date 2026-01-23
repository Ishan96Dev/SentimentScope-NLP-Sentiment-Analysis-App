# Changelog

All notable changes to **SentimentScope - NLP Sentiment Analysis App** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0] - 2026-01-24

### ✨ Added

#### Analytics Dashboard
- **Comprehensive Analytics Dashboard** with aggregated sentiment insights
- **Quick Overview Metrics** displaying total analyses, performance scores, and tracked sentiments
- **Sentiment Distribution Visualizations** with interactive pie charts and breakdowns
- **Word Impact Analysis** showing frequency and sentiment visualization for top 15 words
- **Sentiment Trends Over Time** with interactive time-series charts
  - Polarity trend line chart
  - Confidence level tracking
  - Sentiment distribution over analyses
- **Emotion Analysis Aggregation** with pie charts and confidence metrics
- **Keyword Frequency Tables** for top 10 positive and negative keywords
- **Algorithm Insights Section** explaining DSA implementation details
- **Export Report Functionality** to download comprehensive analytics reports

#### Emotion Detection
- **8 Core Emotion Detection**: Joy, Sadness, Anger, Fear, Surprise, Disgust, Trust, Anticipation
- **Emotion Confidence Scores** for each detected emotion
- **Primary Emotion Identification** with highest confidence score
- **Visual Emotion Distribution** in analytics dashboard
- **Emotion-based Color Coding** in results display

#### Advanced Keyword Extraction
- **Multi-word Key Phrase Support** for better context understanding
- **Frequency-based Keyword Ranking** across all analyses
- **Separate Positive/Negative Keyword Insights** with detailed tables
- **Word-level Sentiment Contribution Analysis** showing impact scores
- **Interactive Word Impact Visualizations** with horizontal bar charts

#### REST API Integration
- **FastAPI-based Backend Service** for programmatic access
- **4 API Endpoints**:
  - `GET /health` - Health check endpoint
  - `POST /analyze` - Single text sentiment analysis
  - `POST /batch` - Batch analysis for multiple texts
  - `GET /stats` - API usage statistics
- **Auto-generated API Documentation** (Swagger UI & ReDoc)
- **Python Client SDK** for easy integration
- **CORS Support** for cross-origin requests
- **Request/Response Models** with Pydantic validation

#### Enhanced Documentation
- **Comprehensive Module Docstrings** with purpose and technical details
- **Analytics Module Documentation** with DSA complexity analysis
- **About Module Documentation** with structured content sections
- **Code Comments** explaining algorithms and data structures

### 🔄 Changed

- **Improved Sentiment Analysis Algorithm** with better confidence calculations
- **Enhanced Visual Polarity Gauge** with emotion indicators
- **Upgraded Session Statistics** to track more detailed metrics
- **Optimized Data Structures** for better performance (O(n*m) complexity)
- **Better Export Functionality** including all new metrics in reports
- **Enhanced UI Layout** with better visual hierarchy in results

### 🐛 Fixed

- **Sidebar Navigation Icons Not Visible** on white/light backgrounds
  - Updated CSS styling for better contrast across all themes
  - Ensured emoji icons remain visible in light mode

### 🔒 Security

- **Enhanced Input Validation** for all new features
- **Rate Limiting Maintained** (10 req/min, 100 req/hour)
- **API Security Headers** for REST endpoints
- **CORS Configuration** for secure cross-origin access

### 📚 Documentation

- Updated README.md with v2.0 features
- Added API documentation and usage examples
- Enhanced code documentation with DSA insights
- Updated security documentation

---

## [1.0] - 2026-01-19

### ✨ Added

#### Core Features
- **Real-time Sentiment Analysis** using TextBlob NLP library
- **Three Sentiment Classifications**: Positive 😊, Neutral 😐, Negative 😠
- **Confidence Scoring** (0-100%) for prediction reliability
- **Polarity Score** (-1 to +1) indicating sentiment direction
- **Subjectivity Score** (0 to 1) measuring opinion vs fact

#### User Interface
- **Streamlit-based Web Application** with clean, modern design
- **Dual-screen Navigation**:
  - 🧠 Sentiment Analyzer (main analysis screen)
  - ℹ️ About App (documentation and guide)
- **Professional Sidebar** with streamlit-option-menu
- **Responsive Design** for desktop and mobile devices
- **Gradient-styled Result Cards** with color coding
- **Dynamic Emoji Indicators** based on sentiment

#### Analysis Features
- **Interactive Polarity Gauge** using Plotly visualization
- **Word-level Sentiment Analysis** showing individual word contributions
- **Sentiment Keywords Extraction** (positive and negative)
- **Quick Example Buttons** for testing (positive/neutral/negative samples)
- **Real-time Character & Word Counter**
- **Analysis History** tracking last 10 analyses
- **Session Statistics** displaying total analyses counter

#### Data Management
- **Export Results** as downloadable text files with timestamp
- **Clear/Reset Functionality** for new analyses
- **Session-based Data Persistence** using Streamlit session state
- **In-memory Storage** (no database required)

#### Security Features
- **Input Validation & Sanitization**
  - Maximum 10,000 characters
  - Maximum 2,000 words
  - Special character filtering
- **Rate Limiting**
  - 10 requests per minute
  - 100 requests per hour
  - 2-second cooldown between requests
- **XSS Protection** with HTML/script tag removal
- **SQL Injection Prevention** with keyword detection
- **Spam Detection** with promotional content filtering
- **Session Management** with 60-minute timeout
- **Security Logging** for all validation events

#### Documentation
- **Comprehensive README.md** with installation and usage instructions
- **About Screen** with detailed sentiment analysis guide
- **Security Documentation** (SECURITY.md) with best practices
- **Contributing Guidelines** (CONTRIBUTING.md)
- **MIT License** (LICENSE)
- **Project Structure Documentation** (STRUCTURE.md)

#### Automation Scripts
- **Setup Scripts** (setup.bat/setup.sh) for automated environment setup
- **Launch Scripts** (run.bat/run.sh) for one-click application start
- **Cross-platform Support** (Windows/Linux/macOS)

### 🔧 Configuration

- **Centralized Configuration** (config.py) for easy customization
- **Environment Variable Support** (.env file)
- **Customizable Thresholds** for sentiment classification
- **Feature Flags** for future enhancements

### 📦 Dependencies

- streamlit==1.28.1
- textblob==0.17.1
- plotly==5.17.0
- streamlit-option-menu==0.3.6
- nltk (for TextBlob corpus)
- python-dotenv (for environment variables)

### 📚 Technical Stack

- **Frontend Framework**: Streamlit
- **NLP Engine**: TextBlob
- **Visualization**: Plotly
- **Language**: Python 3.8+
- **Deployment**: Streamlit Cloud compatible

### 🎯 Use Cases

- Customer Feedback Analysis
- Social Media Monitoring
- Product Review Analysis
- Email Classification
- Content Moderation
- Survey Analysis
- Market Research

---

## Project Information

**Author:** Ishan Chakraborty  
**GitHub:** [@Ishan96Dev](https://github.com/Ishan96Dev)  
**Email:** ishanrock1234@gmail.com  
**License:** MIT  
**Repository:** https://github.com/Ishan96Dev/SentimentScope-NLP-Sentiment-Analysis-App  
**Live Demo:** https://sentimentscope-nlp-sentiment-analysis-app.streamlit.app/

---

## Links

- [Issues](https://github.com/Ishan96Dev/SentimentScope-NLP-Sentiment-Analysis-App/issues)
- [Discussions](https://github.com/Ishan96Dev/SentimentScope-NLP-Sentiment-Analysis-App/discussions)
- [Documentation](docs/overview.md)
- [Security Policy](SECURITY.md)
- [Contributing Guidelines](CONTRIBUTING.md)

---

**© 2026 Ishan Chakraborty | MIT License**
