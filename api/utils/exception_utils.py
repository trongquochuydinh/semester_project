"""
Custom exception classes for business logic and authentication.

Provides specific exception types for different error conditions
to enable precise error handling and user feedback.
"""

class UserAlreadyLoggedInError(Exception):
    """
    Raised when user attempts login while already having active session.
    
    Used to prevent multiple concurrent sessions and enforce
    single-session security policy.
    
    Typical scenarios:
        - User clicks login while already authenticated
        - Session validation detects concurrent login attempt
        - OAuth login when user already has active session
    """
    pass

class TokenExpiredError(Exception):
    """
    Raised when JWT token has expired and needs renewal.
    
    Indicates token lifetime has exceeded configured duration
    and user needs to re-authenticate.
    
    Handling:
        - Clear client-side token storage
        - Redirect to login page
        - Show "session expired" message
    """
    pass

class InvalidTokenError(Exception):
    """
    Raised when JWT token is malformed or has invalid signature.
    
    Indicates token tampering, corruption, or invalid format
    that prevents proper authentication.
    
    Security implications:
        - Possible token manipulation attempt
        - Corrupted client-side storage
        - Configuration mismatch (wrong secret)
    """
    pass

class AuthError(Exception):
    """
    Base class for authentication-related errors.
    
    Parent class for specific authentication failures
    to enable grouped exception handling.
    """
    pass

class InvalidCredentialsError(AuthError):
    """
    Raised when username/password combination is incorrect.
    
    Used for login failures due to wrong credentials
    without revealing whether username or password was wrong.
    
    Security: Prevents username enumeration attacks
    """
    pass

class UserDisabledError(AuthError):
    """
    Raised when user account is disabled/inactive.
    
    Prevents login for accounts that have been administratively
    disabled while preserving user data.
    
    Use cases:
        - Employee termination
        - Account suspension
        - Security incidents
    """
    pass
