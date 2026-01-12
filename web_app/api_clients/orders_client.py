# Import Flask JSON utilities for response formatting
from flask import jsonify
# Import API communication utilities and error handling
from web_app.api_clients.utils import api_post, api_get, APIClientError

# --- Order Data Retrieval Functions ---

def paginate_order(data):
    """
    Get paginated list of orders with filtering and sorting capabilities.
    
    Args:
        data (dict): Pagination and filter parameters including:
            - page (int): Page number to retrieve (starting from 1)
            - size (int): Number of orders per page
            - filters (dict): Search criteria (status, date range, customer, etc.)
            - sort (dict): Sorting preferences (by date, status, total, etc.)
            
    Returns:
        tuple: (response_text, status_code, headers) containing:
            - orders: List of order objects with summary information
            - pagination: Metadata (total_pages, current_page, total_items)
            - filters_applied: Echo of active filters for UI state
            
    Used for: Order management dashboards, order history views, search interfaces
    """
    res = api_post("/api/orders/paginate", data)
    return (res.text, res.status_code, res.headers.items())

def paginate_order_items(order_id, data):
    """
    Get paginated list of items within a specific order.
    
    Args:
        order_id (int): Unique identifier of the order
        data (dict): Pagination parameters for the order items:
            - page (int): Page number for item list
            - size (int): Number of items per page
            - filters (dict): Item-specific filters (category, name, etc.)
            
    Returns:
        tuple: (response_text, status_code, headers) containing:
            - order_items: List of items in the order with quantities and prices
            - pagination: Item pagination metadata
            - order_summary: Basic order information for context
            
    Used for: Order detail views, item management within orders, invoice generation
    """
    res = api_post(f"/api/orders/{order_id}/items/paginate", data)
    return (res.text, res.status_code, res.headers.items())

def orders_this_week():
    """
    Get order statistics and counts for the current week.
    
    Returns:
        dict: Weekly order analytics including:
            - total_orders: Number of orders this week
            - total_revenue: Sum of order values
            - orders_by_status: Breakdown by order status (pending, completed, etc.)
            - daily_breakdown: Orders per day for trend analysis
            - comparison_data: Week-over-week growth metrics
        OR jsonify: Error response if statistics unavailable
        
    Used for: Dashboard widgets, weekly reports, business intelligence
    """
    try:
        res = api_get("/api/orders/order_counts")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

# --- Order Management Functions ---

def create_order(data):
    """
    Create a new order in the system.
    
    Args:
        data (dict): Order creation data including:
            - customer_info: Customer details or customer_id
            - items: List of items with quantities and specifications
            - shipping_address: Delivery location information
            - payment_method: Payment processing details
            - special_instructions: Customer notes or requirements
            - delivery_date: Requested delivery timeframe
            
    Returns:
        jsonify: Success response with order confirmation details:
            - success: True if order created successfully
            - message: Confirmation message for user display
            - order_id: Generated unique identifier for the new order
        OR jsonify: Error response if order creation fails (validation, inventory, etc.)
        
    Used for: Customer order placement, sales team order entry, recurring order creation
    """
    try:
        res = api_post("/api/orders/create", data)
        resp_json = res.json()

        return jsonify({
            "success": True,
            "message": resp_json.get("message")
        })
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def cancel_order(order_id: int):
    """
    Cancel an existing order and handle associated cleanup.
    
    Args:
        order_id (int): Unique identifier of the order to cancel
        
    Returns:
        dict: Cancellation result including:
            - success: Whether cancellation completed
            - message: Status message for user notification
            - refund_info: Payment refund processing details (if applicable)
            - inventory_restored: Items returned to available inventory
        OR jsonify: Error response if cancellation fails (order status, permissions, etc.)
        
    Note: May trigger inventory adjustments, payment refunds, and notification emails
    """
    try:
        res = api_post(f"/api/orders/cancel/{order_id}")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def complete_order(order_id: int):
    """
    Mark an order as completed/fulfilled.
    
    Args:
        order_id (int): Unique identifier of the order to complete
        
    Returns:
        dict: Completion result including:
            - success: Whether order completion was successful
            - message: Confirmation message
            - completion_date: Timestamp of order fulfillment
            - next_actions: Any follow-up tasks (shipping, invoicing, etc.)
        OR jsonify: Error response if completion fails (order status, validation, etc.)
        
    Note: May trigger shipping notifications, invoice generation, and analytics updates
    """
    try:
        res = api_post(f"/api/orders/complete/{order_id}")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code
