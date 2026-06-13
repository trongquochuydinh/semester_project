from flask import jsonify, redirect, session
from typing import Optional

from web_app.api_clients.utils import APIClientError, api_get, api_patch, api_post, api_put


def build_user_session(user_data: dict):
    session["user"] = {
        "id": user_data["id"],
        "username": user_data["username"],
        "role": user_data["role"],
        "oauth_info": user_data.get("oauth_info", {}),
    }
    session["role"] = user_data["role"]
    session["company_id"] = user_data["company_id"]


def login_user(identifier, password):
    try:
        res = api_post("/api/auth/login", {
            "identifier": identifier,
            "password": password
        })

        user_data = res.json()
        session["token"] = user_data["access_token"]
        build_user_session(user_data)

        return jsonify({
            "success": True,
            "user": session["user"]
        })

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

    except Exception as e:
        return jsonify({
            "error": "Unexpected client error",
            "detail": str(e)
        }), 500


def exchange_oauth_code(code: str):
    res = api_post("/api/auth/oauth/exchange", {"code": code})
    user_data = res.json()
    session["token"] = user_data["access_token"]
    build_user_session(user_data)


def oauth_login_success(code: Optional[str]):
    if code:
        exchange_oauth_code(code)
        return

    res = api_get("/api/users/me")
    user_data = res.json()
    build_user_session(user_data)


def logout_user():
    try:
        res = api_post("/api/auth/logout")
        return (res.text, res.status_code, res.headers.items())
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def login_github():
    res = api_get("/api/auth/github/login")
    return res.json()["redirect_url"]


def link_github():
    try:
        res = api_get("/api/auth/github/link")
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
        res = api_get(f"/api/users/{user_id}")
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
        res = api_get("/api/users/stats")
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
        res = api_get("/api/users/roles/assignable")
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
    res = api_post("/api/users/search", data)
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
        res = api_post("/api/users", data)
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
        res = api_put(f"/api/users/{user_id}", data)
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
        res = api_patch(f"/api/users/{user_id}/status")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code