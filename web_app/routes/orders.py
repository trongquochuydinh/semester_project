# Import Flask components for web routing, session management, and request handling
from flask import Blueprint, session, render_template, request

# Import custom authentication decorators for route protection
from web_app.api_clients.utils import token_required, login_required

# Import order-related API client functions with proxy naming to avoid conflicts
from web_app.api_clients.orders_client import (
    paginate_order as proxy_paginate_order,              # Get paginated order list
    paginate_order_items as proxy_paginate_order_items,  # Get items within a specific order
    create_order as proxy_create_order,                  # Create new order functionality
    cancel_order as proxy_cancel_order,                  # Cancel existing order
    complete_order as proxy_complete_order,              # Mark order as completed
    orders_this_week as proxy_orders_this_week           # Get weekly order statistics
)

# Create Blueprint for order-related routes with '/orders' URL prefix
orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

# --- Frontend Template Routes ---

@orders_bp.route('/management')
@login_required  # Requires user to be logged in (session-based auth)
@token_required  # Also requires valid API token for data access
def order_management():
    """
    Render the order management interface page.
    Dual authentication ensures both session and token validity.
    Fallback to login page if user session is invalid.
    """
    # Double-check session validity before rendering management interface
    if session.get('user') is None:
        return render_template('auth_views/login.html')
    
    # Render order management dashboard for authenticated users
    return render_template('management_views/order_management.html')

# --- API Endpoints ---

@orders_bp.route("/paginate", methods=["POST"])
@token_required  # Requires valid API token for access
def paginate_order():
    """
    Get paginated list of orders with optional filtering and sorting.
    Accepts JSON payload with pagination parameters (page, size, filters, etc.).
    Returns structured response with order data and pagination metadata.
    """
    data = request.get_json() or {}  # Get JSON data or empty dict if none provided
    return proxy_paginate_order(data)  # Forward request to API client

@orders_bp.route("<int:order_id>/items/paginate", methods=["POST"])
@token_required  # Requires valid API token for access
def paginate_order_items(order_id: int):
    """
    Get paginated list of items within a specific order.
    
    Args:
        order_id (int): The unique identifier of the order to get items from
    Accepts JSON payload with pagination parameters for the order items.
    """
    data = request.get_json() or {}  # Get JSON data or empty dict if none provided
    return proxy_paginate_order_items(order_id, data)  # Forward to API client with order ID

@orders_bp.route("/create", methods=["POST"])
@token_required  # Requires valid API token for access
def create_order():
    """
    Create a new order.
    Accepts JSON payload with order details (customer info, items, quantities, etc.).
    Returns created order information or error response.
    """
    data = request.get_json() or {}  # Get JSON data or empty dict if none provided
    return proxy_create_order(data)  # Forward request to API client

@orders_bp.route("/cancel/<int:order_id>", methods=["POST"])
@token_required  # Requires valid API token for access
def cancel_order(order_id: int):
    """
    Cancel an existing order.
    
    Args:
        order_id (int): The unique identifier of the order to cancel
    This typically updates order status and may trigger inventory adjustments.
    """
    return proxy_cancel_order(order_id)  # Forward cancellation request to API client

@orders_bp.route("/complete/<int:order_id>", methods=["POST"])
@token_required  # Requires valid API token for access
def complete_order(order_id: int):
    """
    Mark an order as completed/fulfilled.
    
    Args:
        order_id (int): The unique identifier of the order to complete
    This finalizes the order and may trigger shipping/fulfillment processes.
    """
    return proxy_complete_order(order_id)  # Forward completion request to API client

@orders_bp.route("/order_counts")
@token_required  # Requires valid API token for access
def orders_this_week():
    """
    Get order statistics and counts for the current week.
    Returns aggregated data about weekly order volume, revenue, status breakdown, etc.
    Used for dashboard analytics and reporting.
    """
    return proxy_orders_this_week()  # Forward statistics request to API client