# Import standard library modules
import uuid
from datetime import datetime
from typing import List, Optional, Set

# Import SQLAlchemy ORM components for database operations
from sqlalchemy import or_, false
from sqlalchemy.orm import Session, joinedload

# Import application models for database tables
from api.models.user import User
from api.models.role import Role
from api.models.oauth import UserOAuthAccount

# Import custom exception classes
from api.utils import UserAlreadyLoggedInError

# --- User Creation Functions ---

def insert_user(db: Session, user: User):
    """
    Add a new user to the database.
    
    Args:
        db (Session): Database session for transaction management
        user (User): User object to insert with all required fields populated
        
    Note: Uses flush() to get the user ID without committing the transaction
    """
    db.add(user)  # Add user to session
    db.flush()    # Execute INSERT to get user.id, but don't commit

def user_exists_by_username_or_email(
    db: Session,
    *,
    username: str,
    email: str,
    exclude_user_id: Optional[int]
) -> bool:
    """
    Check if a user already exists with the given username or email.
    
    Args:
        db (Session): Database session
        username (str): Username to check for uniqueness
        email (str): Email to check for uniqueness
        exclude_user_id (Optional[int]): User ID to exclude from check (for updates)
        
    Returns:
        bool: True if user exists with matching username or email, False otherwise
        
    Used for: Registration validation, edit form validation
    """
    # Build query to check for existing username or email
    query = db.query(User).filter(
        or_(
            User.username == username,
            User.email == email,
        )
    )

    # Exclude specific user ID (useful when editing existing user)
    if exclude_user_id is not None:
        query = query.filter(User.id != exclude_user_id)

    # Return True if any matching record exists
    return query.first() is not None

# --- User Management Functions ---

def edit_user(
    db: Session,
    user: User,
    updates: dict,
    role_id: int,
) -> User:
    """
    Update existing user information with field validation.
    
    Args:
        db (Session): Database session
        user (User): Existing user object to update
        updates (dict): Dictionary of fields to update
        role_id (int): New role ID to assign to user
        
    Returns:
        User: Updated user object with refreshed data
        
    Security: Only allows updates to predefined safe fields
    """
    # Define which fields can be safely updated
    EDITABLE_FIELDS = {
        "username",   # User's display name
        "email",      # Contact email address
        "company_id"  # Company association for multi-tenant support
    }

    # Apply field updates with validation
    for key, value in updates.items():
        if key in EDITABLE_FIELDS:
            setattr(user, key, value)

    # Apply role update explicitly (security-sensitive field)
    user.role_id = role_id

    # Persist changes and refresh object with latest data
    db.flush()
    db.refresh(user)
    return user

def change_user_is_active(db: Session, user: User, is_active: bool):
    """
    Enable or disable user account (soft delete functionality).
    
    Args:
        db (Session): Database session
        user (User): User to activate/deactivate
        is_active (bool): True to enable account, False to disable
        
    Note: Automatically logs out user when deactivating account
    """
    user.is_active = is_active
    clear_login_session(user)  # Force logout when deactivating
    db.flush()
    db.refresh(user)

# --- Session Management Functions ---

def change_user_status(user: User, status: str):
    """
    Update user's online status and login timestamp.
    
    Args:
        user (User): User object to update
        status (str): New status ("online" or "offline")
        
    Side Effects: Updates last_login timestamp when status changes to "online"
    """
    user.status = status
    if status == "online":
        user.last_login = datetime.now()

def establish_login_session(user: User) -> str:
    """
    Create a new login session for user authentication.
    
    Args:
        user (User): User to create session for
        
    Returns:
        str: Unique session ID for authentication tokens
        
    Raises:
        UserAlreadyLoggedInError: If user already has an active session
        
    Used for: Login process, session token generation
    """
    # Prevent multiple concurrent sessions
    if user.session_id is not None:
        raise UserAlreadyLoggedInError()

    # Generate unique session identifier
    session_id = str(uuid.uuid4())
    user.session_id = session_id
    change_user_status(user, "online")
    return session_id

def clear_login_session(user: User):
    """
    Clear user's active session and set status to offline.
    
    Args:
        user (User): User to log out
        
    Used for: Logout process, account deactivation, security cleanup
    """
    user.session_id = None
    change_user_status(user, "offline")

def clear_login_session_by_user_id(db: Session, user_id: int):
    """
    Log out user by their ID (admin function or security cleanup).
    
    Args:
        db (Session): Database session
        user_id (int): ID of user to log out
        
    Note: Commits transaction immediately for security operations
    """
    user = get_user_data_by_id(db, user_id)
    if user:
        clear_login_session(user)
        db.commit()  # Immediate commit for security actions

# --- User Retrieval Functions ---

def get_user_data_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Fetch complete user data by ID with related information.
    
    Args:
        db (Session): Database session
        user_id (int): Unique user identifier
        
    Returns:
        Optional[User]: User object with role and company data, or None if not found
        
    Performance: Uses joinedload for efficient single-query data retrieval
    """
    return (
        db.query(User)
        .options(
            joinedload(User.role),     # Load role information in same query
            joinedload(User.company),  # Load company information in same query
        )
        .filter(User.id == user_id)
        .first()
    )

def get_user_by_identifier(db: Session, identifier: str) -> Optional[User]:
    """
    Find user by username or email (flexible login support).
    
    Args:
        db (Session): Database session
        identifier (str): Username or email address
        
    Returns:
        Optional[User]: User object with related data, or None if not found
        
    Used for: Login authentication where user can use username or email
    """
    return (
        db.query(User)
        .options(
            joinedload(User.role),     # Load role for authorization
            joinedload(User.company),  # Load company for multi-tenant context
        )
        .filter(
            (User.username == identifier) |
            (User.email == identifier)
        )
        .first()
    )

def get_oauth_providers(db: Session, user_id: int) -> Set[str]:
    """
    Get list of OAuth providers linked to user account.
    
    Args:
        db (Session): Database session
        user_id (int): User to check OAuth connections for
        
    Returns:
        Set[str]: Set of provider names (e.g., {'github', 'google'})
        
    Used for: Account linking UI, login option display
    """
    rows = (
        db.query(UserOAuthAccount.provider)
        .filter(UserOAuthAccount.user_id == user_id)
        .all()
    )
    # Convert query results to set of provider names
    return {row.provider for row in rows}

# --- User Listing and Search Functions ---

def paginate_users(
    db: Session,
    filters: dict,
    allowed_roles: Optional[Set[str]],
    company_id: int,
    limit: int,
    offset: int,
):
    """
    Get paginated list of users with filtering and access control.
    
    Args:
        db (Session): Database session
        filters (dict): Search criteria (status, active state, etc.)
        allowed_roles (Optional[Set[str]]): Roles current user can view (None = superadmin)
        company_id (int): Company scope for multi-tenant filtering
        limit (int): Maximum number of results per page
        offset (int): Number of records to skip for pagination
        
    Returns:
        tuple: (total_count, user_list) for pagination metadata and results
        
    Security: Enforces role-based access control and company isolation
    """
    # Base query with efficient related data loading
    query = (
        db.query(User)
        .options(
            joinedload(User.role),     # Load role names for display
            joinedload(User.company),  # Load company names for display
        )
    )

    # Apply dynamic filters based on request parameters
    for key, value in filters.items():
        if hasattr(User, key):
            query = query.filter(getattr(User, key) == value)

    # Role-based access control
    if allowed_roles is not None:
        if allowed_roles:
            # Restrict to specific roles user is allowed to see
            query = (
                query
                .join(User.role)
                .filter(Role.name.in_(allowed_roles))
            )
        else:
            # Empty set means no access to any users
            query = query.filter(false())

    # Company-based multi-tenant isolation
    if company_id is not None:
        query = query.filter(User.company_id == company_id)

    # Get total count before applying pagination
    total = query.count()
    
    # Apply pagination and get results
    results = query.offset(offset).limit(limit).all()

    return total, results

def count_users(db: Session, company_id=None, online_only=False):
    """
    Get user count with optional filtering for statistics.
    
    Args:
        db (Session): Database session
        company_id (Optional[int]): Limit count to specific company
        online_only (bool): Count only currently online users
        
    Returns:
        int: Number of users matching criteria
        
    Used for: Dashboard statistics, capacity planning, activity monitoring
    """
    query = db.query(User)
    
    # Company-specific filtering
    if company_id is not None:
        query = query.filter(User.company_id == company_id)
    
    # Online status filtering for activity monitoring
    if online_only:
        query = query.filter(User.status == "online")
    
    return query.count()

# --- Database Design Notes ---
# User sessions are managed through session_id field for security
# Multi-tenant isolation enforced through company_id filtering
# OAuth integration supports multiple providers per user
# Soft delete through is_active flag preserves audit trail
# Role-based access control integrated at database query level
