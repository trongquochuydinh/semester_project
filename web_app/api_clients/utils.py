# Import Flask components for JSON responses, session management, and template rendering
from flask import jsonify, session, render_template
from functools import wraps  # Decorator utility for preserving function metadata
import requests  # HTTP client library for API communication
from web_app.config import API_URL  # Backend API base URL configuration

# --- Custom Exception Classes ---

class APIClientError(Exception):
    """
    Custom exception for API communication errors.
    Encapsulates error messages and HTTP status codes for consistent error handling.
    """
    def __init__(self, message, status_code=502):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class APIUnauthorizedError(APIClientError):
    """
    Specialized exception for authentication/authorization failures.
    Inherits from APIClientError but indicates specifically auth-related issues.
    """
    pass

# --- Core API Communication Functions ---

def api_request(method, endpoint, data=None, params=None):
    """
    Generic HTTP request handler for backend API communication.
    Handles authentication, error processing, and session management.
    
    Args:
        method (str): HTTP method (GET, POST, PUT, DELETE, etc.)
        endpoint (str): API endpoint path (with or without leading slash)
        data (dict, optional): JSON payload for POST/PUT requests
        params (dict, optional): URL query parameters for GET requests
        
    Returns:
        requests.Response: HTTP response object from the backend API
        
    Raises:
        APIUnauthorizedError: When authentication fails (401 status)
        APIClientError: For other HTTP errors or network issues
    """
    # Normalize endpoint to ensure it starts with a slash
    endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
    url = f"{API_URL}{endpoint}"
    
    # Set default headers for JSON communication
    headers = {"Content-Type": "application/json"}

    # Add authentication token if user is logged in
    token = session.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        # Make HTTP request with configured parameters
        res = requests.request(
            method.upper(),
            url,
            json=data,           # Automatically serialize dict to JSON
            params=params,       # URL query parameters
            headers=headers,
            # timeout=5          # Uncommented for production use
        )

        # Handle authentication failures
        if res.status_code == 401:
            # Clear invalid session data
            session.pop("token", None)
            session.pop("user", None)
            
            # Raise specific auth error
            raise APIUnauthorizedError(res.text, 401)

        # Handle other HTTP error status codes (4xx, 5xx)
        if res.status_code >= 400:
            try:
                # Extract detailed error message from JSON response
                detail = res.json().get("detail", res.text)
            except Exception:
                # Fallback to raw response text if JSON parsing fails
                detail = res.text
            raise APIClientError(detail, res.status_code)

        return res
        
    except APIUnauthorizedError:
        # Re-raise auth errors without modification
        raise
    except requests.RequestException as e:
        # Handle network errors, timeouts, connection issues
        raise APIClientError(str(e), 502)

def api_get(endpoint, params=None):
    """
    Convenience wrapper for GET requests to the backend API.
    
    Args:
        endpoint (str): API endpoint path
        params (dict, optional): URL query parameters
        
    Returns:
        requests.Response: HTTP response object
    """
    return api_request("get", endpoint, params=params)

def api_post(endpoint, data=None):
    """
    Convenience wrapper for POST requests to the backend API.
    
    Args:
        endpoint (str): API endpoint path
        data (dict, optional): JSON payload to send in request body
        
    Returns:
        requests.Response: HTTP response object
    """
    return api_request("post", endpoint, data=data)

# --- Authentication Decorators ---

def login_required(view_func):
    """
    Decorator to protect routes requiring user authentication.
    Checks for valid user session and redirects to login if not authenticated.
    
    Usage:
        @login_required
        def protected_route():
            return "Protected content"
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # Check if user is logged in (either session user or token exists)
        if session.get("user") is None and session.get("token") is None:
            # Redirect to login page if not authenticated
            return render_template("auth_views/login.html")
        return view_func(*args, **kwargs)
    return wrapper

def token_required(view_func):
    """
    Decorator to protect API endpoints requiring valid authentication token.
    Returns JSON error response if token is missing or invalid.
    
    Usage:
        @token_required
        def api_endpoint():
            return jsonify({"data": "sensitive info"})
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        token = session.get("token")
        if not token:
            # Return JSON error for API calls
            return jsonify({"error": "Not logged in"}), 401
        return view_func(*args, **kwargs)
    return wrapper
