# Import FastAPI components for routing and dependency injection
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

# Import database functions for user operations
from api.db.user_db import get_oauth_providers, get_user_data_by_id

# Import authentication and authorization dependencies
from api.dependencies import get_current_user, require_role, get_db

# Import user model for type hints
from api.models.user import User

# Import request/response schemas for data validation
from api.schemas import (
    LoginRequest, LoginResponse, 
    UserCreateResponse, UserCreateRequest, UserEditResponse, UserEditRequest, UserCountResponse, UserGetResponse,
    RolesResponse, RoleOut, MessageResponse, 
    PaginationRequest, PaginationResponse
)
from api.schemas.user_schema import OAuthInfo

# Import business logic services
from api.services import (
    login_user, 
    get_subroles_for_role, 
    create_user_account, 
    logout_user,  
    get_user_count, 
    get_info_of_user,
    edit_user,
    toggle_user_is_active,
    paginate_users,
    get_current_user_info
)
from api.services.auth_service import handle_github_callback, start_github_link, start_github_login

# Create router for user-related endpoints
router = APIRouter(prefix="/api/users", tags=["users"])

# --- Authentication Endpoints ---

@router.post("/login", response_model=LoginResponse)
def login_user_endpoint(
    request: LoginRequest, 
    db: Session = Depends(get_db)
):
    """
    Authenticate user with username/email and password.
    
    Accepts either username or email as identifier for flexible login.
    Returns JWT access token and user information upon successful authentication.
    
    Args:
        request: Login credentials (identifier + password)
        db: Database session for user lookup and session management
        
    Returns:
        LoginResponse: Access token, user info, and session details
        
    Raises:
        HTTPException 401: Invalid credentials or disabled account
        
    Used for: Web app login, mobile app authentication, API access
    """
    return login_user(request.identifier, request.password, db)

@router.post("/logout", response_model=MessageResponse)
def logout_user_endpoint( 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Log out current authenticated user and invalidate session.
    
    Clears user's session ID to prevent token reuse and updates status to offline.
    
    Args:
        db: Database session for session cleanup
        current_user: Authenticated user from JWT token
        
    Returns:
        MessageResponse: Logout confirmation message
        
    Security: Invalidates JWT tokens by clearing session_id in database
    """
    return logout_user(current_user, db)

# --- OAuth Integration Endpoints ---

@router.get("/auth/github/login")
def github_login():
    """
    Initiate GitHub OAuth login flow for new user authentication.
    
    Generates GitHub OAuth authorization URL with appropriate state parameter
    for security and flow tracking.
    
    Returns:
        dict: GitHub authorization URL for client redirection
        
    OAuth Flow:
        1. Client redirects user to returned URL
        2. User authorizes on GitHub
        3. GitHub redirects to callback with authorization code
        4. Callback endpoint completes authentication
        
    Used for: "Login with GitHub" functionality
    """
    redirect_url = start_github_login()
    return {"redirect_url": redirect_url}

@router.get("/auth/github/link")
def link_github_account(
    current_user = Depends(get_current_user),
):
    """
    Link GitHub account to existing authenticated user.
    
    Allows users to add GitHub as additional authentication method
    to their existing account.
    
    Args:
        current_user: Currently authenticated user to link GitHub account to
        
    Returns:
        dict: GitHub authorization URL for account linking
        
    Security: Requires existing authentication to prevent account takeover
    """
    redirect_url = start_github_link(current_user.id)
    return {"redirect_url": redirect_url}

@router.get("/auth/github/callback")
def github_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):
    """
    Handle GitHub OAuth callback and complete authentication flow.
    
    Processes authorization code from GitHub, exchanges for access token,
    fetches user profile, and either creates new account or links to existing.
    
    Args:
        code: Authorization code from GitHub OAuth redirect
        state: State parameter for security validation
        db: Database session for user creation/linking
        
    Returns:
        RedirectResponse: Redirect to web app with authentication status
        
    Flow Handling:
        - New login: Creates user account + OAuth link
        - Account linking: Adds OAuth link to existing authenticated user
        - Error cases: Redirects with error parameters
    """
    redirect_url = handle_github_callback(code, state, db)
    return RedirectResponse(url=redirect_url)

# --- User Profile and Info Endpoints ---

@router.get("/me")
def get_me_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's profile information.
    
    Returns complete user profile including role, company, and OAuth providers
    for profile display and client-side authorization decisions.
    
    Args:
        db: Database session for OAuth provider lookup
        current_user: Authenticated user from JWT token
        
    Returns:
        dict: User profile with role, company, and linked OAuth providers
        
    Used for: Profile pages, user settings, client-side role checks
    """
    return get_current_user_info(db, current_user)

@router.get("/get_subroles", response_model=RolesResponse)
def get_subroles_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get roles that current user can assign to other users.
    
    Returns roles with lower or equal permissions that the current user
    is authorized to assign during user creation or editing.
    
    Args:
        db: Database session for role lookup
        current_user: Authenticated user to check permissions for
        
    Returns:
        RolesResponse: List of assignable roles
        
    Authorization: Returns roles based on current user's role hierarchy
    Used for: User creation/edit forms, role selection dropdowns
    """
    roles = get_subroles_for_role(
        db=db,
        role_name=current_user.role.name,
        excluded_roles=[current_user.role.name],
    )

    return RolesResponse(
        roles=[RoleOut(name=role.name) for role in roles]
    )

@router.get("/get_user_stats", response_model=UserCountResponse)
def get_user_stats_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user statistics and counts for dashboard analytics.
    
    Returns user counts scoped by current user's permissions and company.
    Superadmins see global stats, regular users see company-specific stats.
    
    Args:
        db: Database session for user count queries
        current_user: Authenticated user for permission scoping
        
    Returns:
        UserCountResponse: Total users, online users, and other statistics
        
    Used for: Dashboard widgets, analytics, system monitoring
    """
    return get_user_count(db, current_user)

# --- User Management Endpoints (Admin/Manager Only) ---

@router.post("/create", response_model=UserCreateResponse)
def create_user_endpoint(
    request : UserCreateRequest, 
    db : Session = Depends(get_db), 
    current_user : User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    """
    Create new user account with role and company assignment.
    
    Creates user with specified role, generates initial password, and assigns
    to appropriate company based on current user's permissions.
    
    Args:
        request: User creation data (username, email, role, etc.)
        db: Database session for user creation
        current_user: Authenticated admin/manager creating the user
        
    Returns:
        UserCreateResponse: Success message and initial password
        
    Authorization:
        - Superadmins: Can create users in any company with any allowed role
        - Admins/Managers: Can create users in their company with lower roles
        
    Security: Initial password generated and returned for admin communication
    """
    return create_user_account(request, db, current_user)

@router.post("/edit/{user_id}", response_model=UserEditResponse)
def edit_user_endpoint(
    user_id: int,
    request : UserEditRequest, 
    db : Session = Depends(get_db),
    current_user : User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    """
    Update existing user information and role assignment.
    
    Allows modification of user profile and role within permission constraints.
    
    Args:
        user_id: ID of user to edit
        request: Updated user data
        db: Database session for user updates
        current_user: Authenticated admin/manager performing edit
        
    Returns:
        UserEditResponse: Update confirmation message
        
    Authorization:
        - Users can only edit users within their company
        - Cannot elevate users to roles higher than their own
        - Superadmins have cross-company edit permissions
    """
    return edit_user(user_id, request, db, current_user)

@router.get("/get/{user_id}", response_model=UserGetResponse)
def get_user_endpoint(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    """
    Get detailed information for specific user.
    
    Returns user profile for admin viewing and editing purposes.
    
    Args:
        user_id: ID of user to retrieve
        db: Database session for user lookup
        current_user: Authenticated admin/manager requesting user info
        
    Returns:
        UserGetResponse: User profile with role and company information
        
    Authorization: Can only view users within same company (unless superadmin)
    Used for: User detail pages, edit form pre-population
    """
    return get_info_of_user(user_id, db, current_user)

@router.post("/toggle_user_is_active/{user_id}", response_model=MessageResponse)
def toggle_user_is_active_endpoint(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    """
    Enable or disable user account (soft delete functionality).
    
    Toggles user's active status to enable/disable login without deleting data.
    Automatically logs out user when disabling account.
    
    Args:
        user_id: ID of user to enable/disable
        db: Database session for status update
        current_user: Authenticated admin/manager performing action
        
    Returns:
        MessageResponse: Status change confirmation
        
    Security: Disabled users cannot log in but data is preserved for audit
    Used for: Account suspension, employee offboarding, security incidents
    """
    return toggle_user_is_active(user_id, db, current_user)

# --- User Listing and Search Endpoints ---

@router.post("/paginate", response_model=PaginationResponse)
def paginate_users_endpoint(
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get paginated list of users with filtering and search capabilities.
    
    Returns users scoped by current user's company and role permissions
    with support for filtering, sorting, and pagination.
    
    Args:
        request: Pagination parameters (page, size, filters, sort)
        db: Database session for user queries
        current_user: Authenticated user for permission scoping
        
    Returns:
        PaginationResponse: Paginated user list with metadata
        
    Features:
        - Multi-tenant filtering by company
        - Role-based result filtering
        - Search by username, email, status
        - Sorting by various fields
        
    Used for: User management tables, search interfaces, admin dashboards
    """
    return paginate_users(
        db=db,
        limit=request.limit,
        offset=request.offset,
        filters=request.filters,
        user_role=current_user.role.name,
        company_id=current_user.company_id,
    )