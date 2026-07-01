"""
JWT Authentication Module - Production Skeleton
Implements JWT token validation, bearer token extraction, and security utilities.

Note: This is a framework implementation. For production deployment:
1. Use a proper secret key management service (AWS Secrets Manager, HashiCorp Vault)
2. Implement user management and role-based access control (RBAC)
3. Add token refresh mechanisms
4. Implement rate limiting per user/API key
5. Add audit logging for all authentication events
"""

from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
import os
from enum import Enum

# ============================================================================
# CONFIGURATION (Should use environment variables in production)
# ============================================================================

# Secret key - In production, load from secure secrets manager
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production-ONLY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# In production, use a proper database for user management
MOCK_USERS = {
    "demo_user": {
        "user_id": "user_001",
        "email": "demo@example.com",
        "role": "viewer",
        "permissions": ["read:battery", "read:supply_chain", "read:fleet"]
    },
    "admin_user": {
        "user_id": "user_admin",
        "email": "admin@example.com",
        "role": "admin",
        "permissions": ["read:*", "write:*", "delete:*"]
    }
}


# ============================================================================
# ENUMS AND MODELS
# ============================================================================

class UserRole(str, Enum):
    """User role enumeration"""
    VIEWER = "viewer"           # Read-only access
    ANALYST = "analyst"         # Read + export
    OPERATIONS = "operations"   # Fleet management
    ADMIN = "admin"             # Full access


class Permission(str, Enum):
    """API permission enumeration"""
    READ_BATTERY = "read:battery"
    READ_SUPPLY_CHAIN = "read:supply_chain"
    READ_FLEET = "read:fleet"
    WRITE_FLEET = "write:fleet"
    READ_REPORTS = "read:reports"
    WRITE_REPORTS = "write:reports"
    ADMIN = "admin:*"


# ============================================================================
# TOKEN UTILITIES
# ============================================================================

def create_access_token(
    user_id: str,
    user_email: str,
    role: UserRole,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        user_id: Unique user identifier
        user_email: User email address
        role: User role
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token as string
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.utcnow() + expires_delta
    
    payload = {
        "sub": user_id,
        "email": user_email,
        "role": role.value,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    try:
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise Exception(f"Token creation failed: {str(e)}")


def create_refresh_token(user_id: str, user_email: str) -> str:
    """Create a JWT refresh token (longer expiration)."""
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload = {
        "sub": user_id,
        "email": user_email,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID"
            )
        
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


# ============================================================================
# DEPENDENCY INJECTION - AUTH DEPENDENCIES
# ============================================================================

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Dependency: Extract and validate JWT from Authorization header.
    
    Usage in route:
        @router.get("/protected")
        async def protected_route(current_user: Dict = Depends(get_current_user)):
            return {"user_id": current_user["sub"]}
    
    Returns:
        Decoded token payload containing user info
    """
    token = credentials.credentials
    return verify_token(token)


async def get_current_user_optional(
    authorization: Optional[str] = Header(None)
) -> Optional[Dict[str, Any]]:
    """
    Dependency: Extract JWT from header if present (optional auth).
    
    Returns None if no token provided, or decoded payload if valid token.
    """
    if not authorization:
        return None
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        return verify_token(token)
    except (ValueError, HTTPException):
        return None


async def require_role(required_role: UserRole):
    """
    Dependency factory: Require specific user role.
    
    Usage in route:
        @router.delete("/admin-only")
        async def admin_route(
            current_user: Dict = Depends(get_current_user),
            _: None = Depends(require_role(UserRole.ADMIN))
        ):
            return {"message": "Admin access granted"}
    """
    async def check_role(current_user: Dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        
        if user_role != required_role.value and user_role != UserRole.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {required_role.value}"
            )
        
        return current_user
    
    return check_role


async def require_permission(required_permission: str):
    """
    Dependency factory: Require specific permission.
    
    Usage in route:
        @router.post("/write-fleet")
        async def write_route(
            current_user: Dict = Depends(get_current_user),
            _: None = Depends(require_permission(Permission.WRITE_FLEET.value))
        ):
            return {"message": "Write access granted"}
    """
    async def check_permission(current_user: Dict = Depends(get_current_user)):
        # In production, fetch actual permissions from database
        user_role = current_user.get("role")
        
        # Admin has all permissions
        if user_role == UserRole.ADMIN.value:
            return current_user
        
        # For demo: mock permission check
        # In production: query permissions table
        if required_permission.startswith("read:"):
            # All authenticated users can read
            return current_user
        elif required_permission.startswith("write:"):
            if user_role not in [UserRole.ANALYST.value, UserRole.OPERATIONS.value, UserRole.ADMIN.value]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: {required_permission}"
                )
        
        return current_user
    
    return check_permission


# ============================================================================
# MOCK AUTHENTICATION (For demo/testing)
# ============================================================================

def get_mock_user_token(username: str) -> str:
    """
    Get a mock JWT token for demo purposes.
    
    Usage (for testing):
        token = get_mock_user_token("demo_user")
        headers = {"Authorization": f"Bearer {token}"}
    """
    if username not in MOCK_USERS:
        raise ValueError(f"Mock user '{username}' not found")
    
    user = MOCK_USERS[username]
    return create_access_token(
        user_id=user["user_id"],
        user_email=user["email"],
        role=UserRole(user.get("role", "viewer"))
    )


# ============================================================================
# PRODUCTION IMPLEMENTATION NOTES
# ============================================================================

"""
TO IMPLEMENT FULL JWT AUTHENTICATION:

1. User Management:
   - Create users table (PostgreSQL)
   - Hash passwords with bcrypt
   - Implement login/signup endpoints
   
2. Token Management:
   - Use database for token blacklisting (logout)
   - Implement refresh token rotation
   - Add token expiration policies per role
   
3. RBAC (Role-Based Access Control):
   - Define permissions per role in database
   - Implement permission checking middleware
   - Add audit logging
   
4. Security Best Practices:
   - Use environment variables for secrets
   - Implement HTTPS only
   - Add rate limiting per user
   - Implement IP whitelisting for admin
   - Use API keys for service-to-service auth
   
5. OAuth2/SSO Integration:
   - Google OAuth
   - Azure AD
   - SAML 2.0
   
6. Monitoring:
   - Log all auth failures
   - Alert on suspicious patterns
   - Track token usage per user
"""
