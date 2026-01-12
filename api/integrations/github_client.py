import requests

from api.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

def exchange_code_for_token(code: str) -> str:
    """
    Exchange GitHub OAuth authorization code for access token.
    
    This is the second step of GitHub's OAuth flow after user authorization.
    The authorization code is exchanged for an access token that can be used
    to make authenticated requests to GitHub's API on behalf of the user.
    
    Args:
        code (str): Authorization code received from GitHub OAuth callback
        
    Returns:
        str: GitHub access token for authenticated API requests
        
    Raises:
        requests.HTTPError: If GitHub API request fails (invalid code, expired code, etc.)
        KeyError: If GitHub response doesn't contain expected access_token field
        
    OAuth Flow Context:
        1. User clicks "Login with GitHub" 
        2. User redirected to GitHub for authorization
        3. GitHub redirects back with authorization code
        4. This function exchanges code for access token
        5. Access token used to fetch user profile information
        
    Used for: OAuth login completion, GitHub account linking
    """
    # Make POST request to GitHub's token exchange endpoint
    res = requests.post(
        "https://github.com/login/oauth/access_token",  # GitHub OAuth token endpoint
        headers={"Accept": "application/json"},          # Request JSON response format
        data={
            "client_id": GITHUB_CLIENT_ID,               # OAuth app client ID
            "client_secret": GITHUB_CLIENT_SECRET,       # OAuth app client secret  
            "code": code,                                # Authorization code from callback
        },
    )
    
    # Raise exception if request failed (4xx or 5xx status codes)
    res.raise_for_status()
    
    # Extract access token from JSON response
    return res.json()["access_token"]


def fetch_user(access_token: str) -> dict:
    """
    Retrieve GitHub user profile information using access token.
    
    Fetches the authenticated user's public profile data from GitHub API.
    This information is used for account creation/linking and profile display.
    
    Args:
        access_token (str): Valid GitHub access token from OAuth flow
        
    Returns:
        dict: GitHub user profile data including:
            - id: GitHub user ID (unique identifier)
            - login: GitHub username  
            - email: User's primary email (may be None if private)
            - name: User's display name
            - avatar_url: Profile picture URL
            - html_url: GitHub profile URL
            - Other public profile fields
            
    Raises:
        requests.HTTPError: If GitHub API request fails (invalid token, rate limits, etc.)
        
    Privacy Note: Only public profile information is returned.
    Private email addresses may not be included unless user grants email scope.
    
    Used for: User profile creation, account linking verification, profile updates
    """
    # Make GET request to GitHub's user API endpoint
    res = requests.get(
        "https://api.github.com/user",                   # GitHub user profile endpoint
        headers={
            "Authorization": f"Bearer {access_token}",   # OAuth access token for authentication
            "Accept": "application/json",                # Request JSON response format
        },
    )
    
    # Raise exception if request failed (invalid token, rate limits, etc.)
    res.raise_for_status()
    
    # Return complete user profile data as dictionary
    return res.json()

# --- GitHub OAuth Integration Design Notes ---
# This module implements GitHub's OAuth 2.0 flow for user authentication:
# 
# OAuth Flow:
# 1. User initiates login → redirect to GitHub authorization
# 2. User grants permission → GitHub redirects with authorization code  
# 3. exchange_code_for_token() → converts code to access token
# 4. fetch_user() → retrieves user profile with access token
# 5. Application creates/links user account based on profile data
#
# Security Considerations:
# - Client credentials stored securely in configuration
# - Access tokens have limited lifetime and scope
# - Only public profile information is accessed
# - Rate limiting handled by GitHub (may need retry logic for production)
#
# Error Handling:
# - Network errors propagated as requests.HTTPError
# - Invalid responses may raise KeyError or ValueError
# - Caller responsible for handling OAuth-specific errors (expired codes, etc.)
