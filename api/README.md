# SentimentScope API Documentation

## Quick Start

### Installation

```bash
# Install API dependencies
pip install fastapi uvicorn pydantic requests
```

### Start Server

```bash
# From project root
python -m uvicorn api.api_server:app --reload --port 8000

# Or run directly
python api/api_server.py
```

### Access Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

## API Endpoints

### 1. Health Check

**Endpoint**: `GET /api/v1/health`

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-01-24T10:30:45.123456"
}
```

### 2. Analyze Single Text

**Endpoint**: `POST /api/v1/analyze`

**Request**:
```json
{
  "text": "I love this amazing product!",
  "include_emotions": true,
  "include_keywords": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "label": "Positive",
    "confidence": 87.5,
    "polarity": 0.625,
    "subjectivity": 0.8,
    "emoji": "😊",
    "color": "#10b981",
    "emotions": {
      "primary_emotion": "Joy",
      "confidence": 85.3,
      "top_emotions": [
        {"emotion": "joy", "score": 85.3},
        {"emotion": "trust", "score": 42.1}
      ]
    },
    "advanced_keywords": {
      "noun_phrases": ["amazing product"],
      "frequent_words": ["love", "amazing", "product"],
      "total_keywords": 3
    }
  },
  "timestamp": "2026-01-24T10:30:45.123456",
  "processing_time_ms": 12.45
}
```

### 3. Batch Analysis

**Endpoint**: `POST /api/v1/batch`

**Request**:
```json
{
  "texts": [
    "This is wonderful!",
    "I'm disappointed.",
    "It works fine."
  ],
  "include_emotions": true,
  "include_keywords": true
}
```

**Response**:
```json
{
  "success": true,
  "results": [
    {
      "label": "Positive",
      "confidence": 85.0,
      "emotions": {"primary_emotion": "Joy", ...},
      ...
    },
    ...
  ],
  "total_processed": 3,
  "timestamp": "2026-01-24T10:30:45.123456",
  "processing_time_ms": 34.12
}
```

### 4. Statistics

**Endpoint**: `GET /api/v1/stats`

**Response**:
```json
{
  "success": true,
  "data": {
    "api_version": "1.0.0",
    "endpoints_available": 4,
    "features": [
      "Single text analysis",
      "Batch processing",
      "Emotion detection",
      "Advanced keyword extraction"
    ]
  },
  "timestamp": "2026-01-24T10:30:45.123456"
}
```

---

## Python Client

### Basic Usage

```python
from api.api_client import SentimentScopeClient

# Initialize
client = SentimentScopeClient(base_url="http://localhost:8000")

# Health check
health = client.health_check()
print(health)

# Analyze text
result = client.analyze("I love this!")
print(result['data']['label'])           # "Positive"
print(result['data']['emotions'])        # {...}

# Batch analysis
results = client.batch_analyze([
    "Great product!",
    "Not good at all.",
    "It's okay."
])
print(results['total_processed'])        # 3
```

---

## cURL Examples

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Analyze Text
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I love this!",
    "include_emotions": true,
    "include_keywords": true
  }'
```

### Batch Analysis
```bash
curl -X POST http://localhost:8000/api/v1/batch \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Great!", "Bad!", "Okay."],
    "include_emotions": true,
    "include_keywords": true
  }'
```

---

## JavaScript/Fetch Example

```javascript
// Analyze text
async function analyzeSentiment(text) {
  const response = await fetch('http://localhost:8000/api/v1/analyze', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      text: text,
      include_emotions: true,
      include_keywords: true
    })
  });
  
  const data = await response.json();
  return data;
}

// Usage
analyzeSentiment("I love this product!").then(result => {
  console.log(result.data.label);      // "Positive"
  console.log(result.data.emotions);   // {...}
});
```

---

## Error Handling

### 404 Not Found
```json
{
  "success": false,
  "error": "Endpoint not found",
  "timestamp": "2026-01-24T10:30:45.123456"
}
```

### 500 Server Error
```json
{
  "success": false,
  "error": "Internal server error",
  "timestamp": "2026-01-24T10:30:45.123456"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "Text cannot be empty",
      "type": "value_error"
    }
  ]
}
```

---

## Rate Limiting (Future)

Currently, API has no rate limits. Future versions will implement:
- API key authentication
- Per-key rate limits
- Usage tracking

---

## CORS Support

CORS is enabled for all origins by default. In production, configure:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Deployment

### Production Server

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn api.api_server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Future)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "api.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Testing

```bash
# Run API client example
python api/api_client.py

# Expected output:
# ======================================================================
# SENTIMENTSCOPE API CLIENT EXAMPLE
# ======================================================================
# 
# 1. Health Check
# Status: healthy
# ...
```

---

## Support

For issues or questions:
- **Email**: ishanrock1234@gmail.com
- **GitHub**: [@Ishan96Dev](https://github.com/Ishan96Dev)

---

**Version**: 1.0.0  
**Last Updated**: January 24, 2026  
**License**: MIT
