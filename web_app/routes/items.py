# Import Flask components for web routing, session management, and request handling
from flask import Blueprint, session, render_template, request

# Import custom authentication decorators for route protection
from web_app.api_clients.utils import token_required, login_required

# Import item-related API client functions with proxy naming to avoid conflicts
from web_app.api_clients.items_client import (
    create_item as proxy_create_item,                    # Item creation functionality
    get_item as proxy_get_item,                         # Fetch individual item data
    edit_item as proxy_edit_item,                       # Update item information
    paginate_item as proxy_paginate_item,               # Get paginated item list
    toggle_item_is_active as proxy_toggle_item_is_active # Enable/disable items (naming inconsistency - should be toggle_item_is_active)
)

# Create Blueprint for item-related routes with '/items' URL prefix
items_bp = Blueprint('items', __name__, url_prefix='/items')

# --- Frontend Template Routes ---

@items_bp.route('/management')
@login_required  # Requires user to be logged in (session-based auth)
def item_management():
    """
    Render the item management interface page.
    This is a frontend template route for administrative item/product management.
    """
    # Double-check session validity before rendering management interface
    if session.get('user') is None:
        return render_template('auth_views/login.html')  # Fallback to login if session invalid
    
    # Render item management dashboard for authenticated users
    return render_template('management_views/item_management.html')

# --- API Endpoints ---

@items_bp.route("/create", methods=["POST"])
@token_required  # Requires valid API token for access
def create_item():
    """
    Create a new item/product.
    Accepts JSON payload with item details (name, description, price, category, etc.).
    """
    data = request.get_json()  # Extract JSON data from request body
    return proxy_create_item(data)  # Forward request to API client

@items_bp.route("/get/<int:item_id>")
@token_required  # Requires valid API token for access
def get_item(item_id):
    """
    Fetch details for a specific item by ID.
    
    Args:
        item_id (int): The unique identifier of the item to retrieve
    """
    return proxy_get_item(item_id)

@items_bp.route("/edit/<int:item_id>", methods=["POST"])
@token_required  # Requires valid API token for access
def edit_item(item_id):
    """
    Update an existing item's information.
    
    Args:
        item_id (int): The unique identifier of the item to update
    Accepts JSON payload with updated item data.
    """
    data = request.get_json()  # Extract JSON data from request body
    return proxy_edit_item(item_id, data)  # Forward to API client with ID and data

@items_bp.route("/toggle_item_is_active/<int:item_id>", methods=["POST"])
@token_required  # Requires valid API token for access
def toggle_item_active(item_id):
    """
    Toggle an item's active status (enable/disable item in catalog).
    
    Args:
        item_id (int): The unique identifier of the item to toggle
    This is a soft delete - item data is preserved but item becomes unavailable for orders.
    """
    return proxy_toggle_item_is_active(item_id)

@items_bp.route("/paginate", methods=["POST"])
@token_required  # Requires valid API token for access
def paginate_item():
    """
    Get paginated list of items with optional filtering and sorting.
    Accepts JSON payload with pagination parameters (page, size, filters, search terms, etc.).
    Returns structured response with item data and pagination metadata.
    Used for displaying product catalogs, inventory management, and search results.
    """
    data = request.get_json() or {}  # Get JSON data or empty dict if none provided
    return proxy_paginate_item(data)  # Forward request to API client