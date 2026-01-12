# Import necessary Flask components and custom modules
from flask import Flask, jsonify, session, request, redirect, url_for
from web_app.config import FLASK_SECRET_KEY, CANONICAL_HOST
from web_app.api_clients.utils import APIUnauthorizedError

# Initialize Flask application instance
app = Flask(__name__)

# Configure Flask application security settings
app.config.update(
    SECRET_KEY=FLASK_SECRET_KEY,  # Secret key for session encryption
    SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access to session cookies (XSS protection)
    SESSION_COOKIE_SAMESITE="Lax",  # CSRF protection while allowing some cross-site requests
    SESSION_COOKIE_SECURE=False  # Allow cookies over HTTP (set to True for HTTPS in production)
)

# Global error handler for API authorization errors
@app.errorhandler(APIUnauthorizedError)
def handle_api_unauthorized(e):
    """
    Handle unauthorized API access errors.
    Returns JSON response for API calls, redirects to home for web requests.
    """
    # Return JSON error for AJAX/API requests
    if request.is_json:
        return jsonify({"error": "Session expired"}), 401

    # Redirect to home page for regular web requests
    return redirect(url_for("auth.home"))

# Middleware to enforce canonical hostname
@app.before_request
def enforce_canonical_host():
    """
    Redirect all requests to the canonical host to prevent duplicate content issues.
    Useful for SEO and ensuring consistent domain usage.
    """
    if request.host != CANONICAL_HOST:
        return redirect(
            f"{request.scheme}://{CANONICAL_HOST}{request.full_path}",
            code=301  # Permanent redirect
        )

# Language switching endpoint
@app.route('/set_language')
def set_language():
    """
    Allow users to change their language preference.
    Stores language preference in session and redirects back to previous page.
    """
    lang = request.args.get('lang')  # Get language code from query parameter
    session['lang'] = lang  # Store language preference in user session
    return redirect(request.referrer or '/')  # Return to previous page or home

# --- Register blueprints ---
# Import all route blueprints for modular application structure
from web_app.routes.context import context_bp      # Global context and utilities
from web_app.routes.auth import auth_bp            # Authentication routes
from web_app.routes.users import users_bp          # User management routes
from web_app.routes.companies import companies_bp  # Company management routes
from web_app.routes.items import items_bp          # Item/product routes
from web_app.routes.orders import orders_bp        # Order processing routes

# Register all blueprints with the Flask application
app.register_blueprint(context_bp)    # Global context routes
app.register_blueprint(auth_bp)       # Authentication endpoints
app.register_blueprint(users_bp)      # User CRUD operations
app.register_blueprint(companies_bp)  # Company management
app.register_blueprint(items_bp)      # Product catalog
app.register_blueprint(orders_bp)     # Order processing

# Application entry point when run directly
if __name__ == '__main__':
    # Start development server on all interfaces, port 8000
    app.run(host="0.0.0.0", port=8000)  # host="0.0.0.0" allows external connections