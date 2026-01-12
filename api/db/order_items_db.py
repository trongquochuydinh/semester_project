# Import SQLAlchemy ORM components for database operations and relationship loading
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc

# Import models for order items and related entities
from api.models.order_item import OrderItem
from api.models.item import Item

def paginate_order_items(
    db: Session,
    order_id: int,
    company_id: int,
    limit: int,
    offset: int,
):
    """
    Get paginated list of items within a specific order with pricing details.
    
    Args:
        db (Session): Database session for query execution
        order_id (int): Unique identifier of the order to get items from
        company_id (int): Company context for multi-tenant security
        limit (int): Maximum number of items per page
        offset (int): Number of items to skip for pagination
        
    Returns:
        tuple: (total_count, results) where results contain:
            - Item: Product information (name, description, etc.)
            - ordered_quantity: Quantity ordered for this specific order
            - unit_price: Price per unit at time of order (historical pricing)
            
    Used for: Order detail views, invoice generation, order editing interfaces
    Security: Company-based filtering ensures multi-tenant data isolation
    """
    # Build query joining order items with product information
    query = (
        db.query(
            Item,                                          # Product details
            OrderItem.quantity.label("ordered_quantity"),  # Quantity in this order
            OrderItem.unit_price.label("unit_price"),      # Historical price
        )
        .join(OrderItem, OrderItem.item_id == Item.id)    # Join items with order_items
        .options(joinedload(Item.company))                # Load company info efficiently
        .filter(OrderItem.order_id == order_id)           # Filter to specific order
    )

    # Apply multi-tenant security filtering
    if company_id is not None:
        query = query.filter(Item.company_id == company_id)

    # Get total count and paginated results
    total = query.count()
    results = query.offset(offset).limit(limit).all()

    return total, results

def insert_order_item(db: Session, order_item: OrderItem):
    """
    Add a new item to an order with quantity and pricing information.
    
    Args:
        db (Session): Database session
        order_item (OrderItem): Order item object with:
            - order_id: Which order this item belongs to
            - item_id: Which product is being ordered
            - quantity: How many units are ordered
            - unit_price: Price per unit (captured at order time)
            
    Note: Uses flush() to persist immediately without committing transaction
    Used for: Adding items during order creation, order modification
    """
    db.add(order_item)
    db.flush()  # Persist to database but don't commit transaction

def get_order_items(db: Session, order_id: int):
    """
    Retrieve all items associated with a specific order.
    
    Args:
        db (Session): Database session
        order_id (int): Order to get items for
        
    Returns:
        List[OrderItem]: All order items for the specified order
        
    Used for: Order processing, fulfillment, order total calculations
    Note: Returns raw OrderItem objects without joined Item details
    """
    return (
        db.query(OrderItem)
        .filter(OrderItem.order_id == order_id)
        .all()
    )

# --- Order Items Design Notes ---
# OrderItem stores historical pricing (unit_price) for audit trail
# Quantity tracking separate from main Item inventory
# Company-based filtering ensures multi-tenant data security
# Efficient joins used for display purposes while maintaining data integrity