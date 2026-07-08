"""
FastAPI Backend for EV Supply Chain & Asset Intelligence Platform
Entry point for all API services
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
import logging
from datetime import datetime

# Import routes
from routes.battery import router as battery_router
from routes.supply_chain import router as supply_chain_router
from routes.fleet import router as fleet_router
from routes.advanced_features import router as advanced_features_router
from routes.analytics import router as analytics_router
from routes.quality import router as quality_router

# Import middleware and services
from middleware import setup_middleware
from services.battery_service import BatteryService
from services.supply_chain_service import SupplyChainService
from services.fleet_service import FleetService
from metrics import get_metrics_collector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="EV Supply Chain & Asset Intelligence API",
    description="AI-powered platform for industrial EV fleet management and supply chain visibility",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup all middleware (error handling, security, rate limiting, etc.)
setup_middleware(app)

# CORS Configuration (already handled by middleware, but keep for compatibility)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(battery_router, prefix="/api/v1", tags=["Battery & Health"])
app.include_router(supply_chain_router, prefix="/api/v1", tags=["Supply Chain"])
app.include_router(fleet_router, prefix="/api/v1", tags=["Fleet Management"])
app.include_router(quality_router, prefix="/api/v1/quality", tags=["Manufacturing Quality"])
app.include_router(advanced_features_router, tags=["Advanced Features"])
app.include_router(analytics_router, tags=["Analytics"])

# Import and include technical validation router
from routes.technical_validation import router as technical_validation_router
app.include_router(technical_validation_router, tags=["Technical Validation"])


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "operational",
        "service": "EV Supply Chain & Asset Intelligence API",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "battery": "/api/v1/battery",
            "supply_chain": "/api/v1/supply-chain",
            "fleet": "/api/v1/fleet",
            "advanced_features": "/api/v1/scenarios, /api/v1/anomalies, /api/v1/alerts, /api/v1/benchmarks"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring with cache and performance stats"""
    try:
        from utils.response import get_performance_metrics
        from utils.cache import get_cache
        
        cache_stats = get_cache().get_stats()
        perf_metrics = get_performance_metrics().get_all_stats()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "cache": cache_stats,
            "performance": {
                "endpoints_monitored": len(perf_metrics)
            }
        }
    except Exception as e:
        # Fallback if utils not available
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat()
        }


@app.get("/api/v1/metrics")
async def get_api_metrics():
    """Get API performance and cache metrics"""
    try:
        from utils.response import get_performance_metrics
        from utils.cache import get_cache
        
        cache_stats = get_cache().get_stats()
        perf_metrics = get_performance_metrics().get_all_stats()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "cache": cache_stats,
            "performance": perf_metrics,
            "recommendation": "Good performance" if cache_stats.get("hit_rate_percent", 0) > 30 else "Consider enabling caching"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics error: {str(e)}")


@app.get("/metrics", response_class=PlainTextResponse)
async def get_prometheus_metrics():
    """
    Prometheus metrics endpoint in OpenMetrics text format
    
    This endpoint exposes platform metrics suitable for scraping by Prometheus
    
    Example Prometheus configuration:
    ```yaml
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'ev-platform'
        static_configs:
          - targets: ['localhost:8000']
        metrics_path: '/metrics'
    ```
    
    Common alerts:
    - High error rate: rate(ev_errors_total[5m]) > 0.05
    - Slow response: ev_response_time_ms > 500
    - Platform down: up == 0
    """
    metrics_collector = get_metrics_collector()
    return metrics_collector.get_metrics_prometheus()


@app.get("/metrics/json")
async def get_metrics_json():
    """
    Metrics endpoint in JSON format for programmatic consumption
    
    Alternative to Prometheus format for systems that prefer JSON
    """
    metrics_collector = get_metrics_collector()
    return metrics_collector.get_metrics_json()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.utcnow().isoformat()},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
