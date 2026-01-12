# Import FastAPI components for routing and dependency injection
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

# Import authentication and authorization dependencies
from api.dependencies import get_current_user, require_role, get_db
from api.models.user import User

# Import request/response schemas for order operations
from api.schemas import(
    PaginationRequest,
    OrderCreateRequest,
    MessageResponse
)

# Import business logic services for order management
from api.services import (
    paginate_orders,
    paginate_order_items,
    create_order,
    cancel_order,
    complete_order,
    count_orders_by_status
)

# Create router for order-related endpoints
router = APIRouter(prefix="/api/orders", tags=["orders"])

# --- Order Listing and Analytics Endpoints ---

@router.post("/paginate")
def paginate_orders_endpoint(
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"])),
):
    """
    Get paginated list of orders with filtering and search capabilities.
    
    Returns orders scoped to current user's company with support for status
    filtering, date ranges, and sorting options.
    
    Args:
        request: Pagination parameters including:
            - limit: Orders per page
            - offset: Orders to skip for pagination
            - filters: Search criteria (status, date range, customer, etc.)
        db: Database session for order queries
        current_user: Authenticated admin/manager user
        
    Returns:
        PaginationResponse: Paginated order list with formatted dates
        
    Features:
        - Multi-tenant filtering by user's company
        - Status-based filtering (pending, processing, completed, etc.)
        - Date range filtering for time-based analysis
        - Formatted timestamps for UI display
        - Sorting by creation date, status, completion date
        
    Authorization: Admin/Manager only - prevents unauthorized order access
    Used for: Order management dashboards, order history, fulfillment tracking
    """
    return paginate_orders(
        db=db,
        limit=request.limit,
        offset=request.offset,
        filters=request.filters,
        company_id=current_user.company_id,
    )

@router.post("/{order_id}/items/paginate")
def paginate_order_items_endpoint(
    order_id: int,
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"])),
):
    """
    Get paginated list of items within a specific order.
    
    Returns detailed item information for order fulfillment, invoice generation,
    and order review purposes with historical pricing.
    
    Args:
        order_id: Unique identifier of order to get items from
        request: Pagination parameters for item list
        db: Database session for order item queries
        current_user: Authenticated admin/manager user
        
    Returns:
        PaginationResponse: Paginated list of items in order with:
            - Item details (name, description, company)
            - Ordered quantity for this specific order
            - Unit price at time of order (historical pricing)
        
    Security: 
        - Multi-tenant validation ensures order belongs to user's company
        - Historical pricing preserved for audit and billing accuracy
        
    Used for: Order detail views, invoice generation, fulfillment processing,
             order editing interfaces, pricing analysis
    """
    return paginate_order_items(
        db=db,
        order_id=order_id,
        company_id=current_user.company_id,
        limit=request.limit,
        offset=request.offset,
    )

@router.get("/order_counts")
def get_order_counts_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get order statistics and counts grouped by status for analytics.
    
    Returns order breakdown for dashboard widgets and business intelligence.
    Data scoped based on user permissions and company context.
    
    Args:
        db: Database session for order count queries
        current_user: Authenticated user for permission and company scoping
        
    Returns:
        dict: Order counts grouped by status with additional analytics:
            - Orders by status (pending, processing, completed, cancelled)
            - Time-based filtering support
            - Company-scoped or global data based on user role
        
    Authorization:
        - Superadmins: See global order statistics
        - Regular users: See company-specific statistics
        
    Used for: Dashboard widgets showing order status breakdown,
             business intelligence, performance monitoring, trend analysis
    """
    return count_orders_by_status(
        db=db,
        current_user=current_user,
    )

# --- Order Management Endpoints (Admin/Manager Only) ---

@router.post("/create", response_model=MessageResponse)
def create_order_endpoint(
    data: OrderCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"])),
):
    """
    Create new customer order with specified items and quantities.
    
    Processes order creation with inventory validation, pricing capture,
    and multi-tenant assignment to current user's company.
    
    Args:
        data: Order creation data including:
            - order_type: Classification (standard, rush, bulk, etc.)
            - items: List of items with quantities
            - customer information and delivery details
        db: Database session for order creation
        current_user: Authenticated admin/manager creating order
        
    Returns:
        MessageResponse: Order creation confirmation
        
    Business Logic:
        - Order created in "created" status initially  
        - Items captured with current pricing (historical preservation)
        - Inventory levels may be reserved or decremented
        - Order automatically assigned to user's company
        - Created by current user for tracking
        
    Authorization: Admin/Manager only - prevents unauthorized order creation
    Used for: Sales order entry, customer order placement, bulk order processing
    """
    return create_order(
        db=db,
        data=data,
        current_user=current_user,
    )

@router.post("/cancel/{order_id}")
def cancel_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"])),
):
    """
    Cancel existing order and handle associated cleanup.
    
    Changes order status to cancelled and may trigger inventory restoration,
    payment refunds, and notification processes.
    
    Args:
        order_id: ID of order to cancel
        db: Database session for order updates
        current_user: Authenticated admin/manager performing cancellation
        
    Returns:
        dict: Cancellation result with status update confirmation
        
    Business Impact:
        - Order status changed to "cancelled"
        - Inventory may be restored to available stock
        - Payment refund processes may be initiated
        - Customer notifications may be triggered
        - Audit trail preserved for business analysis
        
    Authorization: Admin/Manager only - prevents unauthorized cancellations
    Multi-tenant: Can only cancel orders within user's company
    Used for: Order management, customer service, inventory corrections
    """
    return cancel_order(
        db=db,
        order_id=order_id,
        current_user=current_user,
    )

@router.post("/complete/{order_id}")
def complete_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"])),
):
    """
    Mark order as completed/fulfilled and finalize processing.
    
    Updates order status to completed with completion timestamp and may
    trigger final business processes like invoicing and analytics updates.
    
    Args:
        order_id: ID of order to complete
        db: Database session for order updates
        current_user: Authenticated admin/manager completing order
        
    Returns:
        dict: Completion result with timestamp and status confirmation
        
    Business Impact:
        - Order status changed to "completed"
        - Completion timestamp recorded for analytics
        - Final invoice generation may be triggered
        - Shipping notifications may be sent
        - Revenue recognition processes may be initiated
        - Performance metrics updated
        
    Authorization: Admin/Manager only - prevents unauthorized completions
    Multi-tenant: Can only complete orders within user's company
    Used for: Order fulfillment, shipping confirmation, delivery completion
    """
    return complete_order(
        db=db,
        order_id=order_id,
        current_user=current_user,
    )