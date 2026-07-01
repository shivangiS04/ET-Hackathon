"""
Middleware for error handling, logging, and security
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
import logging
import traceback
from typing import Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for consistent error handling and logging"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        """
        Handle exceptions and standardize error responses.
        Also records metrics for Prometheus.
        """
        from metrics import get_metrics_collector
        import time
        
        try:
            # Log incoming request
            logger.info(f"➡️  {request.method} {request.url.path}")
            
            # Record start time for metrics
            start_time = time.time()
            
            response = await call_next(request)
            
            # Record metrics
            duration_ms = (time.time() - start_time) * 1000
            metrics_collector = get_metrics_collector()
            metrics_collector.record_request(request.url.path, duration_ms, response.status_code)
            
            # Log successful response
            if response.status_code < 400:
                logger.info(f"✅ {request.method} {request.url.path} - Status: {response.status_code} - {duration_ms:.2f}ms")
            else:
                logger.warning(f"⚠️  {request.method} {request.url.path} - Status: {response.status_code}")
                metrics_collector.record_error(f"http_{response.status_code}")
            
            return response
        
        except ValueError as e:
            """Validation errors - 400 Bad Request"""
            logger.warning(f"❌ Validation Error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Validation Error",
                    "detail": str(e),
                    "timestamp": datetime.utcnow().isoformat(),
                    "path": request.url.path,
                }
            )
        
        except KeyError as e:
            """Missing required fields - 400 Bad Request"""
            logger.warning(f"❌ Missing Field: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Missing Required Field",
                    "detail": f"Required field not found: {str(e)}",
                    "timestamp": datetime.utcnow().isoformat(),
                    "path": request.url.path,
                }
            )
        
        except TypeError as e:
            """Type errors - 400 Bad Request"""
            logger.warning(f"❌ Type Error: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Type Error",
                    "detail": f"Invalid data type: {str(e)}",
                    "timestamp": datetime.utcnow().isoformat(),
                    "path": request.url.path,
                }
            )
        
        except Exception as e:
            """Catch-all for unhandled exceptions - 500 Internal Server Error"""
            logger.error(f"❌ Unhandled Exception: {str(e)}")
            logger.error(traceback.format_exc())
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal Server Error",
                    "detail": "An unexpected error occurred. Please contact support.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "path": request.url.path,
                }
            )


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware - simple in-memory implementation"""
    
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}  # {ip: [timestamps]}
    
    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        """Check rate limits and proceed if allowed"""
        
        client_ip = request.client.host
        now = datetime.now().timestamp()
        
        # Clean old requests (older than 1 minute)
        if client_ip in self.requests:
            self.requests[client_ip] = [
                ts for ts in self.requests[client_ip]
                if now - ts < 60
            ]
        else:
            self.requests[client_ip] = []
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            logger.warning(f"⚠️  Rate limit exceeded for {client_ip}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate Limit Exceeded",
                    "detail": f"Maximum {self.requests_per_minute} requests per minute allowed",
                    "retry_after": 60,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )
        
        # Record this request
        self.requests[client_ip].append(now)
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            self.requests_per_minute - len(self.requests[client_ip])
        )
        response.headers["X-RateLimit-Reset"] = str(int(now + 60))
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Validate incoming requests"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        
        # Validate content type for POST/PUT requests
        if request.method in ["POST", "PUT"]:
            content_type = request.headers.get("content-type", "")
            
            if not content_type.startswith("application/json"):
                logger.warning(f"❌ Invalid content type: {content_type}")
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": "Invalid Content-Type",
                        "detail": "Expected 'application/json'",
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
        
        response = await call_next(request)
        return response


class CORSHeadersMiddleware(BaseHTTPMiddleware):
    """Handle CORS properly"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        
        # Handle preflight requests
        if request.method == "OPTIONS":
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",
                    "Access-Control-Max-Age": "3600",
                }
            )
        
        response = await call_next(request)
        
        # Add CORS headers to all responses
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response


def setup_middleware(app):
    """Register all middleware with the app"""
    
    # Order matters! Security headers should be first
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(CORSHeadersMiddleware)
    app.add_middleware(RequestValidationMiddleware)
    app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
    app.add_middleware(ErrorHandlingMiddleware)
    
    logger.info("✅ All middleware registered successfully")
    logger.info("💡 JWT authentication framework available - see auth.py for production setup")


# ============================================================================
# JWT AUTHENTICATION - PRODUCTION SKELETON
# ============================================================================
# 
# To enable JWT authentication on protected endpoints:
#
# 1. Import in routes:
#    from auth import get_current_user, require_role, Permission, UserRole
#
# 2. Add to protected routes:
#    @router.get("/protected", tags=["Protected"])
#    async def protected_endpoint(current_user = Depends(get_current_user)):
#        '''This endpoint requires valid JWT token'''
#        return {"authenticated_user": current_user["sub"]}
#
# 3. Test with mock token:
#    from auth import get_mock_user_token
#    token = get_mock_user_token("demo_user")
#    # Use token: Authorization: Bearer <token>
#
# For production deployment, see auth.py for:
# - User database integration
# - OAuth2/SSO setup
# - Permission-based access control
# - Token refresh mechanisms
# - Audit logging
# ============================================================================
