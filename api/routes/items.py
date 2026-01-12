# Import FastAPI components for routing and dependency injection
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

# Import authentication and authorization dependencies
from api.dependencies import get_current_user, require_role, get_db
from api.models.user import User

# Import request/response schemas for item operations
from api.schemas import(
    PaginationRequest,
    ItemCreationRequest,
    ItemEditRequest,
    ItemEditResponse
)

# Import business logic services for item management
from api.services import (
    create_item,
    edit_item,
    get_item,
    paginate_items,
    toggle_item_is_active
)

# Create router for item-related endpoints
router = APIRouter(prefix="/api/items", tags=["items"])

# --- Item Listing and Search Endpoints ---

@router.post("/paginate")
def paginate_items_endpoint(
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get paginated list of items with filtering and search capabilities.
    
    Returns items scoped to current user's company with support for various
    filters including low stock alerts, name search, and status filtering.
    
    Args:
        request: Pagination parameters including:
            - limit: Items per page
            - offset: Items to skip for pagination
            - filters: Search criteria (name, low_stock, is_active, etc.)
        db: Database session for item queries
        current_user: Authenticated user for company scoping
        
    Returns:
        PaginationResponse: Paginated item list with metadata
        
    Features:
        - Multi-tenant filtering by user's company
        - Low stock item prioritization (sorted by quantity ascending)
        - Name-based search and filtering
        - Active/inactive status filtering
        - Inventory level filtering
        
    Used for: Product catalogs, inventory management, item selection,
             low stock alerts, order creation interfaces
    """
    return paginate_items(
        db=db,
        limit=request.limit,
        offset=request.offset,
        filters=request.filters,
        company_id=current_user.company_id,
    )

@router.get("/get/{item_id}")
def get_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    """
    Get detailed information for specific item.
    
    Returns complete item profile including pricing, inventory, and metadata
    for admin viewing and editing purposes.
    
    Args:
        item_id: Unique identifier of item to retrieve
        db: Database session for item lookup
        current_user: Authenticated admin/manager user
        
    Returns:
        dict: Item details including name, price, quantity, SKU, and status
        
    Authorization: Admin/Manager only - prevents unauthorized item data access
    Multi-tenant: Can only access items within user's company
    Used for: Item detail pages, edit form pre-population, inventory review
    """
    return get_item(item_id, db, current_user)

# --- Item Management Endpoints (Admin/Manager Only) ---

@router.post("/create")
def create_item_endpoint(
    request: ItemCreationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    """
    Create new item in the product catalog.
    
    Adds new product with pricing, inventory, and company association.
    Item automatically assigned to current user's company.
    
    Args:
        request: Item creation data including:
            - name: Product name/title
            - sku: Stock Keeping Unit (product code)
            - price: Current selling price
            - quantity: Initial inventory quantity
        db: Database session for item creation
        current_user: Authenticated admin/manager creating item
        
    Returns:
        dict: Success message and created item information
        
    Business Logic:
        - Item created with is_active = True (available for orders)
        - Automatically associated with current user's company
        - SKU should be unique within company
        - Price stored with decimal precision for accuracy
        
    Authorization: Admin/Manager only - prevents unauthorized catalog changes
    Used for: Adding new products, inventory expansion, catalog management
    """
    return create_item(request, db, current_user)

@router.post("/edit/{item_id}", response_model=ItemEditResponse)
def edit_item_endpoint(
    item_id: int,
    request: ItemEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    """
    Update existing item information and inventory.
    
    Allows modification of item details including pricing and inventory levels
    with company access validation.
    
    Args:
        item_id: ID of item to update
        request: Updated item data (name, price, quantity)
        db: Database session for item updates
        current_user: Authenticated admin/manager performing update
        
    Returns:
        ItemEditResponse: Update confirmation message
        
    Business Logic:
        - Price changes affect future orders (historical prices preserved)
        - Inventory changes immediately affect availability
        - Only items within user's company can be edited
        
    Authorization: Admin/Manager only - prevents unauthorized price/inventory changes
    Multi-tenant: Can only edit items within user's company
    Used for: Price updates, inventory adjustments, product information maintenance
    """
    return edit_item(item_id, request, db, current_user)

@router.post("/toggle_item_is_active/{item_id}")
def toggle_item_is_active_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin", "manager"]))
):
    """
    Enable or disable item in catalog (soft delete functionality).
    
    Toggles item's active status to control visibility in catalog without
    deleting data. Preserves item information for order history.
    
    Args:
        item_id: ID of item to enable/disable
        db: Database session for status update
        current_user: Authenticated admin/manager performing action
        
    Returns:
        dict: Status change confirmation and new active state
        
    Business Impact:
        - Active items: Available for new orders, visible in catalog
        - Inactive items: Hidden from catalog, preserved for order history
        - Existing orders with inactive items remain unaffected
        
    Authorization: Admin/Manager only - prevents unauthorized catalog changes
    Used for: Seasonal products, discontinued items, product lifecycle management,
             temporary catalog adjustments without data loss
    """
    return toggle_item_is_active(item_id, db, current_user)