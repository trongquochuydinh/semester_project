from typing import List
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from api.dependencies.db import get_db
from api.models.user import User
from api.utils import decode_access_token, decode_token_ignore_exp, InvalidTokenError, TokenExpiredError
from api.db.user_db import get_user_data_by_id, clear_login_session_by_user_id

security = HTTPBearer()

def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    FastAPI dependency that extracts and validates the current authenticated user.
    
    Args:
        token (HTTPAuthorizationCredentials): JWT token from Authorization header
        db (Session): Database session for user data lookup
        
    Returns:
        User: Authenticated user object with role and company information
        
    Raises:
        HTTPException(401): For various authentication failures:
            - Token expired or invalid
            - User not found or disabled
            - Session mismatch or expired
            
    Security Features:
        - JWT token validation with expiration checking
        - Session ID validation to prevent token replay attacks
        - Automatic session cleanup on expired tokens
        - User status validation (active/inactive)
        
    Usage:
        @router.get("/profile")
        def get_profile(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id, "role": current_user.role.name}
    """
    
    try:
        # Decode and validate JWT token
        payload = decode_access_token(token.credentials)

    except TokenExpiredError:
        """
        Handle expired tokens with graceful session cleanup.
        
        When a token expires, we attempt to extract the user ID from the expired token
        and clear their session to ensure security. This prevents the user from being
        stuck in a "logged in" state with an invalid token.
        """
        # Extract user info from expired token for cleanup
        stale_payload = decode_token_ignore_exp(token.credentials)

        if stale_payload:
            user_id = stale_payload.get("sub")
            if user_id:
                # Clear the user's session to force fresh login
                clear_login_session_by_user_id(db, user_id)

        # Return user-friendly error message
        raise HTTPException(
            status_code=401,
            detail="Session expired. Please log in again."
        )

    except InvalidTokenError:
        """
        Handle malformed or tampered tokens.
        
        This catches tokens that are structurally invalid, have invalid signatures,
        or have been tampered with.
        """
        raise HTTPException(status_code=401, detail="Invalid token")

    # Extract user ID from validated token payload
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401)

    # Fetch user data from database
    user = get_user_data_by_id(db, user_id)
    if not user:
        # User not found (possibly deleted after token was issued)
        raise HTTPException(status_code=401)

    # Check if user account is active
    if not user.is_active:
        raise HTTPException(status_code=401, detail="User disabled")

    # Validate session ID to prevent token replay attacks
    token_session_id = payload.get("session_id")
    if not token_session_id or user.session_id != token_session_id:
        """
        Session ID validation prevents security issues:
        - Token replay attacks (using old tokens after logout)
        - Concurrent session conflicts
        - Tokens issued before password changes
        """
        raise HTTPException(status_code=401, detail="Session expired")

    return user

def require_role(required_roles: List[str]):
    """
    Factory function that creates role-based access control dependencies.
    
    Args:
        required_roles (List[str]): List of role names that are allowed access
        
    Returns:
        function: FastAPI dependency function that enforces role requirements
        
    Usage:
        # Single role requirement
        admin_only = require_role(["admin"])
        
        @router.delete("/users/{user_id}")
        def delete_user(
            user_id: int,
            current_user: User = Depends(admin_only)
        ):
            # Only admins can access this endpoint
            pass
            
        # Multiple role requirement
        management_only = require_role(["admin", "manager"])
        
        @router.get("/reports")
        def get_reports(current_user: User = Depends(management_only)):
            # Admins and managers can access this endpoint
            pass
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        """
        Inner dependency function that performs the actual role checking.
        
        Args:
            current_user (User): Authenticated user (injected by get_current_user)
            
        Returns:
            User: The current user if role check passes
            
        Raises:
            HTTPException(403): If user's role is not in required_roles list
        """
        # Get user's role name from the related role object
        role_name = current_user.role.name

        # Check if user's role is in the list of allowed roles
        if role_name not in required_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")

        # Return user for use in route handler
        return current_user

    return role_checker

# --- Authentication Flow Design Notes ---
# 1. Client includes JWT token in Authorization: Bearer <token> header
# 2. get_current_user dependency extracts and validates token
# 3. User information loaded from database with role/company context
# 4. Session validation ensures token hasn't been invalidated
# 5. require_role can add additional authorization layers
#
# Security Features:
# - JWT signature validation prevents token tampering
# - Session ID validation prevents token replay after logout
# - Automatic session cleanup on token expiration
# - Role-based access control for fine-grained permissions
# - User status checking (active/inactive accounts)