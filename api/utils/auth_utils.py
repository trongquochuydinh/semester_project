# Import security and utility libraries
import secrets
import string
from typing import Dict, Optional
from urllib.parse import urlencode
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError as JWTInvalidTokenError
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash

# Import configuration and schemas
from api.config import JWT_SECRET
from api.schemas.user_schema import OAuthStateData
from api.utils.exception_utils import TokenExpiredError, InvalidTokenError

# JWT configuration constants
JWT_ALGORITHM = "HS256"

def create_access_token(user_id: int, role: str, session_id, expires_in: int = 3600) -> str:
    """
    Generate JWT access token for authenticated user.
    
    Creates signed JWT containing user identification and session validation
    data with configurable expiration time.
    
    Args:
        user_id: User's database ID for identification
        role: User's role name for authorization
        session_id: Unique session identifier for security
        expires_in: Token lifetime in seconds (default: 1 hour)
        
    Returns:
        str: Signed JWT token for API authentication
        
    Security Features:
        - Session ID prevents token replay after logout
        - Role included for client-side authorization decisions
        - Expiration prevents indefinite token usage
    """
    payload = {
        "sub": user_id,              # Subject (user ID)
        "role": role,                # User role for authorization
        "session_id": session_id,    # Session validation
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    """
    Decode and validate JWT access token.
    
    Verifies token signature and expiration, returning payload data
    for authenticated requests.
    
    Args:
        token: JWT access token from Authorization header
        
    Returns:
        dict: Token payload with user_id, role, session_id
        
    Raises:
        TokenExpiredError: Token has expired
        InvalidTokenError: Token signature invalid or malformed
    """
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"verify_exp": True},  # Strict expiration checking
            leeway=0,
        )
    except ExpiredSignatureError:
        raise TokenExpiredError()
    except JWTInvalidTokenError:
        raise InvalidTokenError()

def decode_token_ignore_exp(token: str) -> dict:
    """
    Decode JWT token without expiration validation.
    
    Used for extracting user info from expired tokens for cleanup
    operations like session clearing.
    
    Args:
        token: JWT token (may be expired)
        
    Returns:
        dict: Token payload or empty dict if invalid
        
    Security Note: Only use for cleanup operations, never for authentication
    """
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"verify_exp": False},  # Skip expiration check
        )
    except JWTInvalidTokenError:
        return {}

def generate_password(length=10):
    """
    Generate secure random password for new users.
    
    Creates cryptographically secure password using letters and digits
    for initial user account setup.
    
    Args:
        length: Password length (default: 10 characters)
        
    Returns:
        str: Random password for user communication
        
    Security: Uses secrets module for cryptographic randomness
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify plaintext password against stored hash.
    
    Uses secure password hashing comparison to prevent timing attacks
    and validate user credentials.
    
    Args:
        password: User-provided plaintext password
        password_hash: Stored password hash from database
        
    Returns:
        bool: True if password matches, False otherwise
        
    Security: Uses werkzeug's timing-safe comparison
    """
    return check_password_hash(password_hash, password)

# OAuth state management for CSRF protection
_OAUTH_STATE_STORE: Dict[str, OAuthStateData] = {}
_OAUTH_STATE_TTL = timedelta(minutes=10)

def create_oauth_state(user_id: Optional[int]) -> str:
    """
    Create temporary OAuth state for CSRF protection.
    
    Generates secure random state parameter to prevent cross-site
    request forgery during OAuth flows.
    
    Args:
        user_id: User ID for account linking flows (None for login)
        
    Returns:
        str: Random state parameter for OAuth URL
        
    Security Features:
        - Cryptographically secure random generation
        - Time-based expiration (10 minutes)
        - User ID binding for account linking validation
    """
    state = secrets.token_urlsafe(32)

    _OAUTH_STATE_STORE[state] = {
        "user_id": user_id,
        "expires_at": datetime.utcnow() + _OAUTH_STATE_TTL,
    }

    return state

def consume_oauth_state(state: str) -> Optional[int]:
    """
    Validate and consume OAuth state parameter.
    
    Verifies state parameter from OAuth callback and returns associated
    user ID if valid. State is consumed (deleted) to prevent reuse.
    
    Args:
        state: State parameter from OAuth callback URL
        
    Returns:
        Optional[int]: User ID if state valid, None if invalid/expired
        
    Security: Single-use state prevents replay attacks
    """
    data = _OAUTH_STATE_STORE.pop(state, None)

    if not data:
        return None  # State not found

    if data["expires_at"] < datetime.utcnow():
        return None  # State expired

    return data["user_id"]

def oauth_error_redirect(message: str) -> str:
    """
    Generate error redirect URL for OAuth failures.
    
    Creates redirect URL with error message for user notification
    when OAuth flow encounters problems.
    
    Args:
        message: Error description for user display
        
    Returns:
        str: Redirect URL with error parameter
        
    Used for: OAuth callback error handling, user experience
    """
    params = urlencode({"error": message})
    return f"http://localhost:8000/?{params}"