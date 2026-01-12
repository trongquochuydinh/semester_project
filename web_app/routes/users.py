# Import Flask components for web routing and request handling
from flask import Blueprint, request, render_template

# Import custom authentication decorators for route protection
from web_app.api_clients.utils import login_required, token_required

# Import user-related API client functions with proxy naming to avoid conflicts
from web_app.api_clients.users_client import(
    create_user as proxy_create_user,                      # User creation functionality
    get_subroles as proxy_get_subroles,                   # Fetch available user roles/permissions
    get_user_count as proxy_get_user_count,               # Get total user statistics
    get_user as proxy_get_user,                           # Fetch individual user data
    get_my_data as proxy_get_my_data,                     # Get current user's profile data
    edit_user as proxy_edit_user,                         # Update user information
    toggle_user_is_active as proxy_toggle_user_is_active, # Enable/disable user accounts
    paginate_user as proxy_paginate_user                  # Get paginated user list
)

# Create Blueprint for user-related routes with '/users' URL prefix
users_bp = Blueprint('users', __name__, url_prefix='/users')

# --- Frontend Template Routes ---

@users_bp.route('/management')
@login_required  # Requires user to be logged in (session-based auth)
def user_management():
    """
    Render the user management interface page.
    This is a frontend template route for administrative user management.
    """
    return render_template('management_views/user_management.html')

# --- API Endpoints ---

@users_bp.route('/create', methods=['POST'])
@token_required  # Requires valid API token for access
def create_user():
    """
    Create a new user account.
    Accepts JSON payload with user details and forwards to API client.
    """
    data = request.get_json()  # Extract JSON data from request body
    return proxy_create_user(data)  # Forward request to API client

@users_bp.route("/get_my_data")
@token_required  # Requires valid API token for access
def get_my_data():
    """
    Get the current authenticated user's profile data.
    Returns user's own information based on the session token.
    """
    return proxy_get_my_data()

@users_bp.route('/get_subroles')
@token_required  # Requires valid API token for access
def get_subroles():
    """
    Fetch all available user roles and permissions.
    Used for populating role selection dropdowns in user forms.
    """
    return proxy_get_subroles()

@users_bp.route('/get_user_stats')
@token_required  # Requires valid API token for access
def get_user_count():
    """
    Get user statistics and counts.
    Returns aggregated data about total users, active users, etc.
    """
    return proxy_get_user_count()

@users_bp.route("/get/<int:user_id>")
@token_required  # Requires valid API token for access
def get_user(user_id):
    """
    Fetch details for a specific user by ID.
    
    Args:
        user_id (int): The unique identifier of the user to retrieve
    """
    return proxy_get_user(user_id)

@users_bp.route("/edit/<int:user_id>", methods=["POST"])
@token_required  # Requires valid API token for access
def edit_user(user_id):
    """
    Update an existing user's information.
    
    Args:
        user_id (int): The unique identifier of the user to update
    Accepts JSON payload with updated user data.
    """
    data = request.get_json()  # Extract JSON data from request body
    return proxy_edit_user(user_id, data)  # Forward to API client with ID and data

@users_bp.route("/toggle_user_is_active/<int:user_id>", methods=["POST"])
@token_required  # Requires valid API token for access
def toggle_user_is_active(user_id):
    """
    Toggle a user's active status (enable/disable account).
    
    Args:
        user_id (int): The unique identifier of the user to toggle
    This is a soft delete - user data is preserved but account is disabled.
    """
    return proxy_toggle_user_is_active(user_id)

@users_bp.route("/paginate", methods=["POST"])
@token_required  # Requires valid API token for access
def paginate_user():
    """
    Get paginated list of users with optional filtering and sorting.
    Accepts JSON payload with pagination parameters (page, size, filters, etc.).
    Returns a structured response with user data and pagination metadata.
    """
    data = request.get_json() or {}  # Get JSON data or empty dict if none provided
    return proxy_paginate_user(data)
