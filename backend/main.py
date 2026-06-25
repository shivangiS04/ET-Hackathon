"""
FastAPI Backend for EV Supply Chain & Asset Intelligence Platform
Entry point for all API services
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

# Import routes
from routes.battery import router as battery_router
from routes.supply_chain import router as supply_chain_router
from routes.fleet import router as fleet_router

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

# CORS Configuration
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
            "fleet": "/api/v1/fleet"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


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
