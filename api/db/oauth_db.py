# Import SQLAlchemy ORM components for database operations
from sqlalchemy.orm import Session

# Import OAuth account model for external authentication integration
from api.models.oauth import UserOAuthAccount

def get_oauth_account_by_provider_user_id(
    db: Session,
    provider: str,
    provider_user_id: str,
):
    """
    Find existing OAuth account by provider and external user ID.
    
    Args:
        db (Session): Database session for query execution
        provider (str): OAuth provider name (e.g., 'github', 'google', 'microsoft')
        provider_user_id (str): User's unique ID from the OAuth provider
        
    Returns:
        UserOAuthAccount: OAuth account record if found, None otherwise
        
    Used for: OAuth login flow, account linking validation, duplicate prevention
    Critical for preventing account hijacking through OAuth manipulation
    """
    return (
        db.query(UserOAuthAccount)
        .filter_by(
            provider=provider,                  # e.g., 'github'
            provider_user_id=provider_user_id, # GitHub user ID
        )
        .first()
    )

def create_oauth_account(
    db: Session,
    *,
    user_id: int,
    provider: str,
    provider_user_id: str,
    provider_email: str,
):
    """
    Create new OAuth account linking for existing user.
    
    Args:
        db (Session): Database session
        user_id (int): Internal user ID to link OAuth account to
        provider (str): OAuth provider name
        provider_user_id (str): User's unique ID from OAuth provider
        provider_email (str): User's email from OAuth provider (for verification)
        
    Returns:
        UserOAuthAccount: Created OAuth account record
        
    Used for: Account linking process, new OAuth registration
    Security: Links external OAuth identity to internal user account
    """
    # Create new OAuth account linkage
    oauth = UserOAuthAccount(
        user_id=user_id,                      # Link to internal user
        provider=provider,                    # OAuth provider (github, google, etc.)
        provider_user_id=provider_user_id,    # External user ID
        provider_email=provider_email,        # Email from OAuth (for verification)
    )
    
    # Add to database and commit immediately
    db.add(oauth)
    db.commit()  # Commit immediately for security-critical operation
    
    return oauth

# --- OAuth Integration Design Notes ---
# Each user can have multiple OAuth providers linked (github + google)
# provider_user_id is the unique identifier from external service
# provider_email stored for verification and account recovery
# Immediate commit on creation ensures OAuth state consistency
# Critical for security: prevents account takeover through OAuth manipulation
