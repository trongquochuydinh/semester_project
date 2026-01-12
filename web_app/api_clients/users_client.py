# Import Flask utilities for redirects, session management, and JSON responses
from flask import redirect, session, jsonify
from typing import Optional  # Type hinting for optional parameters

# Import API communication utilities and error handling
from web_app.api_clients.utils import api_post, api_get, APIClientError

# --- Session Management Functions ---

def build_user_session(user_data: dict):
    """
    Populate Flask session with user data from API response.
    Centralizes session structure for consistency across login methods.
    
    Args:
        user_data (dict): User information from backend API containing:
            - id: User's unique identifier
            - username: User's display name
            - role: User's permission level
            - company_id: Associated company for multi-tenant support
            - oauth_info: GitHub/OAuth connection data (optional)
    
    Used by: Password login, OAuth login, account linking
    """
    # Store structured user information in session
    session["user"] = {
        "id": user_data["id"],
        "username": user_data["username"],
        "role": user_data["role"],
        "oauth_info": user_data.get("oauth_info", {}),  # Optional OAuth data
    }

    # Store frequently accessed fields at session root for convenience
    session["role"] = user_data["role"]           # For authorization checks
    session["company_id"] = user_data["company_id"]  # For multi-tenant filtering

# --- Authentication Functions ---

def login_user(identifier, password):
    """
    Authenticate user with username/email and password.
    
    Args:
        identifier (str): Username or email address
        password (str): User's password
        
    Returns:
        jsonify: Success response with user session data
        OR jsonify: Error response with authentication failure details
    """
    try:
        # Send login credentials to backend API
        res = api_post("/api/users/login", {
            "identifier": identifier,
            "password": password
        })

        user_data = res.json()

        # Store authentication token for subsequent API calls
        session["token"] = user_data["access_token"]
        
        # Build user session from API response
        build_user_session(user_data)

        # Return success response with user information
        return jsonify({
            "success": True,
            "user": session["user"]
        })

    except APIClientError as e:
        # Return API-specific error (invalid credentials, account disabled, etc.)
        return jsonify({"error": e.message}), e.status_code

    except Exception as e:
        # Handle unexpected errors (network issues, malformed responses)
        return jsonify({
            "error": "Unexpected client error",
            "detail": str(e)
        }), 500

def oauth_login_success(token: Optional[str]):
    """
    Complete OAuth authentication flow after successful callback.
    Handles both new OAuth logins and account linking scenarios.
    
    Args:
        token (Optional[str]): Authentication token from OAuth callback
            - Present for new OAuth logins
            - None for account linking (uses existing session token)
    """
    # Store new authentication token (OAuth login scenario)
    if token:
        session["token"] = token

    # Fetch current user data using the token (new login or existing session)
    res = api_get("/api/users/me")
    user_data = res.json()

    # Update session with latest user information
    build_user_session(user_data)

def logout_user():
    """
    Log out the current user and notify backend of session termination.
    
    Returns:
        tuple: (response_text, status_code, headers) from logout API call
        OR jsonify: Error response if logout notification fails
        
    Note: Session cleanup happens in calling code, this only notifies backend
    """
    try:
        res = api_post("/api/users/logout")
        return (res.text, res.status_code, res.headers.items())
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

# --- OAuth Integration Functions ---

def login_github():
    """
    Initiate GitHub OAuth login flow.
    
    Returns:
        str: GitHub OAuth authorization URL for user redirection
        
    The returned URL should be used to redirect the user to GitHub for authentication.
    """
    res = api_get("/api/users/auth/github/login")
    redirect_url = res.json()["redirect_url"]
    return redirect_url

def link_github():
    """
    Link existing user account with GitHub OAuth.
    Allows users to add GitHub authentication to their existing account.
    
    Returns:
        redirect: Flask redirect response to GitHub OAuth flow
        OR jsonify: Error response if linking initiation fails
    """
    try:
        res = api_get("/api/users/auth/github/link")
        redirect_url = res.json()["redirect_url"]
        return redirect(redirect_url)
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

# --- User Data Management Functions ---

def get_my_data():
    """
    Fetch current authenticated user's profile information.
    
    Returns:
        dict: User profile data from API
        OR jsonify: Error response if user data unavailable
    """
    try:
        res = api_get("/api/users/me")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def get_user(user_id):
    """
    Fetch profile information for a specific user (admin function).
    
    Args:
        user_id (int): Unique identifier of user to retrieve
        
    Returns:
        dict: User profile data
        OR jsonify: Error response if user not found or access denied
    """
    try:
        res = api_get(f"/api/users/get/{user_id}")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def get_user_count():
    """
    Get user statistics and aggregated counts (admin function).
    
    Returns:
        dict: User statistics including total users, active users, etc.
        OR jsonify: Error response if statistics unavailable
    """
    try:
        res = api_get("/api/users/get_user_stats")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def get_subroles():
    """
    Fetch available user roles/permissions for the current user's context.
    
    Returns:
        tuple: (response_text, status_code, headers) with available roles
        OR jsonify: Error response if roles unavailable
        
    Used for: Role selection dropdowns in user creation/editing forms
    """
    try:
        res = api_get("/api/users/get_subroles")
        return (res.text, res.status_code, res.headers.items())
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def paginate_user(data):
    """
    Get paginated list of users with filtering and sorting options.
    
    Args:
        data (dict): Pagination parameters including page, size, filters, sort
        
    Returns:
        tuple: (response_text, status_code, headers) with paginated user list
    """
    res = api_post("/api/users/paginate", data)
    return (res.text, res.status_code, res.headers.items())

# --- User Management Functions ---

def create_user(data):
    """
    Create a new user account (admin function).
    
    Args:
        data (dict): User creation data including username, email, role, etc.
        
    Returns:
        jsonify: Success response with confirmation and initial password
        OR jsonify: Error response if creation fails
    """
    try:
        res = api_post("/api/users/create", data)
        resp_json = res.json()

        return jsonify({
            "success": True,
            "message": resp_json.get("message"),
            "initial_password": resp_json.get("initial_password")  # For admin notification
        })
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def edit_user(user_id, data):
    """
    Update existing user information (admin function).
    
    Args:
        user_id (int): Unique identifier of user to update
        data (dict): Updated user data (supports partial updates)
        
    Returns:
        jsonify: Success response with confirmation message
        OR jsonify: Error response if update fails
    """
    try:
        res = api_post(f"/api/users/edit/{user_id}", data)
        resp_json = res.json()

        return jsonify({
            "success": True,
            "message": resp_json.get("message")
        })
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def toggle_user_is_active(user_id):
    """
    Toggle user's active status - enable/disable account (admin function).
    
    Args:
        user_id (int): Unique identifier of user to toggle
        
    Returns:
        dict: Updated user status information
        OR jsonify: Error response if toggle fails
        
    Note: This is a soft delete - preserves user data but prevents login
    """
    try:
        res = api_post(f"/api/users/toggle_user_is_active/{user_id}")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code