from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc
from api.models.item import Item

LOW_STOCK_THRESHOLD = 20

def insert_item(db: Session, item: Item):
    """
    Add a new item to the product catalog.
    
    Args:
        db (Session): Database session for transaction management
        item (Item): Item object with all required fields populated
        
    Note: Uses flush() to get item ID immediately for related operations
    Used for: Product catalog expansion, inventory setup, bulk imports
    """
    db.add(item)
    db.flush()  # Persist to get item.id without committing transaction

def apply_stock_change(db: Session, item: Item, delta: int):
    """
    Adjust item inventory quantity (positive or negative changes).
    
    Args:
        db (Session): Database session
        item (Item): Item to adjust inventory for
        delta (int): Change in quantity (positive = increase, negative = decrease)
        
    Used for: Order fulfillment (negative), restocking (positive), inventory adjustments
    Note: Caller responsible for validation and business logic
    """
    item.quantity += delta  # Apply inventory change
    db.flush()              # Persist change immediately

def get_item_data_by_id(db: Session, item_id: int):
    """
    Retrieve complete item information by ID with company context.
    
    Args:
        db (Session): Database session
        item_id (int): Unique item identifier
        
    Returns:
        Item: Item object with company data loaded, or None if not found
        
    Used for: Item detail views, order processing, inventory management
    Performance: Uses joinedload for efficient single-query data retrieval
    """
    return (
        db.query(Item)
        .options(
            joinedload(Item.company),  # Load company info for multi-tenant context
        )
        .filter(Item.id == item_id)
        .first()
    )

def edit_item(
    db: Session,
    item_id: int,
    updates: dict,
) -> Optional[Item]:
    """
    Update existing item information with field validation.
    
    Args:
        db (Session): Database session
        item_id (int): Item to update
        updates (dict): Fields to update with new values
        
    Returns:
        Optional[Item]: Updated item object, or None if item not found
        
    Security: Only allows updates to predefined safe fields
    """
    # Define which fields can be safely updated
    EDITABLE_FIELDS = {
        "name",      # Item name/title
        "price",     # Current selling price
        "quantity"   # Inventory quantity
    }

    # Find item to update
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return None

    # Apply validated field updates
    for key, value in updates.items():
        if key in EDITABLE_FIELDS:
            setattr(item, key, value)

    # Persist changes
    db.flush()
    return item

def change_item_is_active(item: Item, is_active: bool):
    """
    Enable or disable item in catalog (soft delete functionality).
    
    Args:
        item (Item): Item to activate/deactivate
        is_active (bool): True to make item available, False to hide from catalog
        
    Used for: Product lifecycle management, seasonal items, discontinued products
    Note: Preserves item data for order history while controlling availability
    """
    item.is_active = is_active

def paginate_items(
    db: Session,
    filters: dict,
    company_id: int,
    limit: int,
    offset: int,
):
    """
    Get paginated list of items with filtering and special sorting options.
    
    Args:
        db (Session): Database session
        filters (dict): Search and filter criteria including:
            - low_stock: Show only items with quantity <= LOW_STOCK_THRESHOLD
            - name: Partial name matching
            - is_active: Active/inactive status
            - Other item fields for exact matching
        company_id (int): Company context for multi-tenant filtering
        limit (int): Maximum items per page
        offset (int): Items to skip for pagination
        
    Returns:
        tuple: (total_count, items_list) for pagination and results
        
    Special Features: Low stock items are sorted by quantity ascending for priority
    """
    # Base query with efficient company data loading
    query = (
        db.query(Item)
        .options(
            joinedload(Item.company),  # Load company info for context
        )
    )

    # Special handling for low stock filter with priority sorting
    if filters.get("low_stock"):
        query = (
            query
            .filter(
                Item.quantity <= LOW_STOCK_THRESHOLD,  # Low stock threshold
                Item.is_active == True                 # Only active items
            )
            .order_by(asc(Item.quantity))             # Lowest stock first
        )

    # Apply remaining filters (skip special filters already handled)
    for key, value in filters.items():
        if key in {"low_stock"}:  # Skip already processed filters
            continue

        if hasattr(Item, key):
            query = query.filter(getattr(Item, key) == value)

    # Multi-tenant security: restrict to user's company
    if company_id is not None:
        query = query.filter(Item.company_id == company_id)

    # Get count and paginated results
    total = query.count()
    results = query.offset(offset).limit(limit).all()

    return total, results

# --- Item Management Design Notes ---
# Item lifecycle: active (available) ↔ inactive (hidden from catalog)
# Inventory tracking through quantity field with delta-based updates
# Low stock alerts through threshold-based filtering and sorting
# Multi-tenant isolation through company_id filtering
# Soft delete preserves data integrity for historical orders
# Special sorting for operational priorities (low stock first)
