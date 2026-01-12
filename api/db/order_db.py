# Import type hints and SQLAlchemy components
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

# Import models for orders and related entities
from api.models import Order, User

def paginate_order(
    db: Session,
    filters: dict,
    company_id: int,
    limit: int,
    offset: int,
):
    """
    Get paginated list of orders with filtering and formatted display data.
    
    Args:
        db (Session): Database session for query execution
        filters (dict): Search criteria including status, date ranges, customer info
        company_id (int): Company context for multi-tenant filtering
        limit (int): Maximum orders per page
        offset (int): Number of orders to skip for pagination
        
    Returns:
        tuple: (total_count, orders_list) with formatted datetime fields added
        
    Post-processing: Adds human-readable formatted dates for UI display
    """
    # Base query with efficient company data loading
    query = (
        db.query(Order)
        .options(
            joinedload(Order.company),  # Load company info for display/filtering
        )
    )

    # Apply dynamic filters based on search criteria
    for key, value in filters.items():
        if hasattr(Order, key):
            query = query.filter(getattr(Order, key) == value)

    # Multi-tenant security: restrict to user's company
    if company_id is not None:
        query = query.filter(Order.company_id == company_id)

    # Get count and paginated results
    total = query.count()
    results = query.offset(offset).limit(limit).all()

    # Add formatted datetime fields for UI display (non-persistent)
    for order in results:
        # Format creation date for display (DD.MM.YYYY HH:MM)
        order.created_at_fmt = (
            order.created_at.strftime("%d.%m.%Y %H:%M")
            if order.created_at else None
        )
        # Format completion date for display
        order.completed_at_fmt = (
            order.completed_at.strftime("%d.%m.%Y %H:%M")
            if order.completed_at else None
        )

    return total, results

def insert_order(db: Session, order: Order):
    """
    Create a new order in the database.
    
    Args:
        db (Session): Database session
        order (Order): Order object with all required fields populated
        
    Note: Uses flush() to get order ID immediately for order item creation
    Used for: Order creation workflow, bulk order imports
    """
    db.add(order)
    db.flush()  # Get order.id without committing transaction

def get_order_by_id(db: Session, order_id: int) -> Optional[Order]:
    """
    Retrieve complete order information by ID.
    
    Args:
        db (Session): Database session
        order_id (int): Unique order identifier
        
    Returns:
        Optional[Order]: Order with company data loaded, or None if not found
        
    Used for: Order detail views, order processing, status updates
    """
    return (
        db.query(Order)
        .options(
            joinedload(Order.company),  # Load company for context
        )
        .filter(Order.id == order_id)
        .first()
    )

def change_order_status(order: Order, status: str):
    """
    Update order status for workflow management.
    
    Args:
        order (Order): Order object to update
        status (str): New status ("pending", "processing", "shipped", "completed", "cancelled")
        
    Note: Does not automatically update timestamps - handle in business logic
    Used for: Order lifecycle management, fulfillment tracking
    """
    order.status = status

def count_orders(
    db: Session,
    company_id: int,
    filters: dict,
) -> int:
    """
    Count orders matching specific criteria for statistics and reporting.
    
    Args:
        db (Session): Database session
        company_id (int): Company context (mandatory for multi-tenant security)
        filters (dict): Filtering criteria including:
            - status: Order status filter
            - from_ts: Start date for time range
            - to_ts: End date for time range
            
    Returns:
        int: Number of orders matching all criteria
        
    Used for: Dashboard statistics, reporting, analytics
    """
    query = db.query(func.count(Order.id))

    # Company scope is mandatory for data isolation
    query = query.filter(Order.company_id == company_id)

    # Apply status filtering if specified
    status = filters.get("status")
    if status is not None:
        query = query.filter(Order.status == status)

    # Apply time range filters for date-based reporting
    from_ts = filters.get("from_ts")
    to_ts = filters.get("to_ts")

    if from_ts is not None:
        query = query.filter(Order.created_at >= from_ts)

    if to_ts is not None:
        query = query.filter(Order.created_at <= to_ts)

    return query.scalar()

def count_orders_grouped_by_status(
    db: Session,
    company_id: int,
    is_superadmin: bool,
    filters: dict,
):
    """
    Get order counts grouped by status for dashboard analytics.
    
    Args:
        db (Session): Database session
        company_id (int): Company context for regular users
        is_superadmin (bool): Whether user can see all companies' data
        filters (dict): Additional filtering criteria:
            - from_ts/to_ts: Date range filters
            - order_type: Type of orders to include
            
    Returns:
        List[tuple]: List of (status, count) tuples for each order status
        
    Used for: Dashboard widgets showing order status breakdown
    Security: Respects superadmin privileges for cross-company reporting
    """
    # Build query to count orders grouped by status
    query = db.query(
        Order.status,
        func.count(Order.id).label("count")
    )

    # Apply company filtering unless user is superadmin
    if not is_superadmin:
        query = query.filter(Order.company_id == company_id)

    # Apply optional time range filters
    if "from_ts" in filters:
        query = query.filter(Order.created_at >= filters["from_ts"])

    if "to_ts" in filters:
        query = query.filter(Order.created_at <= filters["to_ts"])

    # Apply optional order type filtering
    if "order_type" in filters:
        query = query.filter(Order.order_type == filters["order_type"])

    # Group by status and return results
    return query.group_by(Order.status).all()

# --- Order Management Design Notes ---
# Order lifecycle: created -> processing -> shipped -> completed
# Alternative flows: created/processing -> cancelled
# Status changes should trigger business logic (inventory, notifications)
# Multi-tenant security enforced at database level
# Formatted dates added for UI without modifying core data