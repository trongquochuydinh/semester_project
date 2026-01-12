# Import Flask components for web routing, request handling, and session management
from flask import Blueprint, abort, redirect, request, session, render_template

# Import authentication-related API client functions with proxy naming to avoid conflicts
from web_app.api_clients.users_client import (
    login_user as proxy_login_user,         # Standard username/password login
    login_github as proxy_login_github,     # GitHub OAuth login flow
    logout_user as proxy_logout_user,       # User logout and session cleanup
    link_github as proxy_link_github,       # Link existing account to GitHub
    oauth_login_success                     # Handle successful OAuth callback
)
from web_app.api_clients.utils import api_get  # Generic API GET request utility

# Create Blueprint for authentication routes (no URL prefix - auth routes at root level)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    """
    Application home page with conditional rendering based on authentication status.
    Serves as the main entry point for both authenticated and unauthenticated users.
    """
    # Get error message from URL parameters (passed from redirects)
    error = request.args.get("error")
    
    # Check if user is logged in by examining session data
    if session.get('user') is None:
        # User not authenticated - render login page
        return render_template(
            'auth_views/login.html',
            error=error  # Pass any error messages to login template
        )

    # User authenticated - render main dashboard/index page
    return render_template('base_views/index.html', error=error)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handle standard username/password authentication.
    Accepts JSON payload with user credentials and forwards to API client.
    """
    data = request.get_json()  # Extract JSON data from request body
    identifier = data.get('identifier')  # Username or email
    password = data.get('password')      # User password
    return proxy_login_user(identifier, password)  # Forward to API client for authentication

@auth_bp.route("/auth/oauth-linked")
@auth_bp.route("/auth/oauth-success")
def oauth_success():
    """
    Handle successful OAuth authentication callback.
    Multiple routes handle different OAuth success scenarios:
    - /auth/oauth-success: New OAuth login
    - /auth/oauth-linked: Account linking completion
    """
    # Extract authentication token from callback URL
    token = request.args.get("token")
    
    # Process the OAuth success and establish user session
    oauth_login_success(token)

    # Redirect to home page after successful authentication
    return redirect("/")

@auth_bp.route("/auth/github/link")
def link_github():
    """
    Initiate GitHub account linking for existing users.
    Allows users to connect their existing account with GitHub OAuth.
    """
    return proxy_link_github()  # Forward to API client to start linking process

@auth_bp.route("/auth/github/login")
def github_login():
    """
    Initiate GitHub OAuth login flow.
    Redirects user to GitHub for authentication.
    """
    # Get GitHub OAuth URL from API client and redirect user
    return redirect(proxy_login_github())

@auth_bp.route('/logout')
def logout():
    """
    Handle user logout with proper session cleanup.
    Includes graceful error handling for API communication issues.
    """
    # Check if user session exists before attempting logout
    if session.get('user'):
        try:
            # Notify API of logout to update user status/tracking
            proxy_logout_user()
        except Exception as e:
            # Log error but don't prevent logout from completing
            print(f"Error updating user status: {e}")
    
    # Clear all session data regardless of API call success
    session.clear()
    
    # Return to login page after logout
    return render_template('auth_views/login.html')