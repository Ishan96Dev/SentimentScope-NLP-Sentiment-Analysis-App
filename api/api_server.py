"""
FastAPI Server for Sentiment Analysis API

Provides REST API endpoints for programmatic access to sentiment analysis.

Endpoints:
- POST /api/v1/analyze - Analyze single text
- POST /api/v1/batch - Analyze multiple texts
- GET /api/v1/health - Health check
- GET /api/v1/stats - Usage statistics

Usage:
    python -m uvicorn api.api_server:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import time

# Import sentiment analyzer
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from sentiment.analyzer import SentimentAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="SentimentScope API",
    description="RESTful API for sentiment analysis and emotion detection",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer
analyzer = SentimentAnalyzer()

# Request/Response models
class AnalyzeRequest(BaseModel):
    """Request model for single text analysis"""
    text: str
    include_emotions: bool = True
    include_keywords: bool = True
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        if len(v) > 10000:
            raise ValueError('Text too long (max 10000 characters)')
        return v


class BatchAnalyzeRequest(BaseModel):
    """Request model for batch text analysis"""
    texts: List[str]
    include_emotions: bool = True
    include_keywords: bool = True
    
    @validator('texts')
    def texts_valid(cls, v):
        if not v or len(v) == 0:
            raise ValueError('Texts list cannot be empty')
        if len(v) > 100:
            raise ValueError('Maximum 100 texts per batch')
        return v


class AnalyzeResponse(BaseModel):
    """Response model for analysis results"""
    success: bool
    data: Dict[str, Any]
    timestamp: str
    processing_time_ms: float


class BatchAnalyzeResponse(BaseModel):
    """Response model for batch analysis"""
    success: bool
    results: List[Dict[str, Any]]
    total_processed: int
    timestamp: str
    processing_time_ms: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str


# API key validation (simplified - in production use proper auth)
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key from header (optional, for rate limiting)"""
    # In production, implement proper API key validation
    # For now, just check if provided
    if x_api_key:
        return x_api_key
    return "anonymous"


# Endpoints
@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns API status and version information.
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
async def analyze_text(
    request: AnalyzeRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze sentiment of a single text
    
    Args:
        request: AnalyzeRequest with text and options
        api_key: API key from header (optional)
        
    Returns:
        AnalyzeResponse with sentiment analysis results
    """
    start_time = time.time()
    
    try:
        # Perform analysis
        result = analyzer.analyze(request.text)
        
        # Filter response based on options
        if not request.include_emotions:
            result.pop('emotions', None)
        if not request.include_keywords:
            result.pop('advanced_keywords', None)
        
        processing_time = (time.time() - start_time) * 1000
        
        return AnalyzeResponse(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat(),
            processing_time_ms=round(processing_time, 2)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/v1/batch", response_model=BatchAnalyzeResponse)
async def batch_analyze(
    request: BatchAnalyzeRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze sentiment of multiple texts in batch
    
    Args:
        request: BatchAnalyzeRequest with list of texts
        api_key: API key from header (optional)
        
    Returns:
        BatchAnalyzeResponse with analysis results for all texts
    """
    start_time = time.time()
    
    try:
        # Perform batch analysis
        results = []
        for text in request.texts:
            result = analyzer.analyze(text)
            
            # Filter based on options
            if not request.include_emotions:
                result.pop('emotions', None)
            if not request.include_keywords:
                result.pop('advanced_keywords', None)
                
            results.append(result)
        
        processing_time = (time.time() - start_time) * 1000
        
        return BatchAnalyzeResponse(
            success=True,
            results=results,
            total_processed=len(results),
            timestamp=datetime.now().isoformat(),
            processing_time_ms=round(processing_time, 2)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")


@app.get("/api/v1/stats")
async def get_stats(api_key: str = Depends(verify_api_key)):
    """
    Get API usage statistics
    
    Returns statistics about API usage (placeholder for future implementation).
    """
    return JSONResponse({
        "success": True,
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
        "timestamp": datetime.now().isoformat()
    })


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(500)
async def server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting SentimentScope API Server...")
    print("📖 API Documentation: http://localhost:8000/api/docs")
    print("📊 ReDoc Documentation: http://localhost:8000/api/redoc")
    uvicorn.run(app, host="0.0.0.0", port=8000)
