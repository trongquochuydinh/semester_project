# Import SQLAlchemy components for ORM model definition
from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Import database base class for model inheritance
from api.db.db_engine import Base

class OrderItem(Base):
    """
    Order item model for individual line items within customer orders.
    
    Represents specific products ordered with quantities and historical pricing.
    Links orders to items while preserving pricing and quantity information
    at the time of order creation.
    
    Features:
        - Many-to-many relationship between orders and items
        - Quantity tracking per order line item
        - Historical pricing preservation (unit_price)
        - Cascade deletion with parent order
        - Precise decimal pricing for financial accuracy
        
    Key Design Principles:
        - Preserves pricing at time of order (audit trail)
        - Separate from current item pricing for historical accuracy
        - Enables order total calculations and financial reporting
        - Supports partial fulfillment and inventory tracking
    """
    __tablename__ = "order_items"

    # --- Primary Key ---
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,               # Unique order item identifier
    )

    # --- Foreign Key Relationships ---
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),  # Delete when parent order deleted
        nullable=False,                 # Must belong to an order
    )

    item_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("items.id", ondelete="CASCADE"),   # Delete when item is deleted
        nullable=False,                 # Must reference a valid item
    )

    # --- Order Line Details ---
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,                 # Number of units ordered (must be > 0)
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(10, 2),                 # Price per unit at time of order
        nullable=False,                 # Historical pricing preserved for audit
    )

    # -------------------------
    # Relationships
    # -------------------------

    order = relationship(
        "Order",
        back_populates="items",         # Access parent order details
    )

    item = relationship(
        "Item",
        back_populates="order_items",   # Access product information
    )

# --- Order Item Design Notes ---
# Historical Pricing:
# - unit_price captures price at time of order creation
# - Preserves pricing even if item.price changes later
# - Essential for accurate financial reporting and customer billing
# - Prevents pricing discrepancies in completed orders
#
# Quantity Management:
# - Represents units ordered, not inventory deduction
# - Inventory adjustments handled in business logic
# - Supports fractional quantities if needed (change to Decimal)
# - Enables partial fulfillment tracking
#
# Cascade Behavior:
# - OrderItems deleted when parent Order is deleted
# - OrderItems deleted when referenced Item is deleted
# - Maintains referential integrity across deletions
# - Consider soft deletes for important audit trails
#
# Financial Calculations:
# - Line total = quantity * unit_price
# - Order total = sum of all order item line totals
# - Use Numeric type for exact decimal arithmetic
# - Avoid float type for financial calculations
#
# Business Intelligence:
# - Enables product sales analysis (which items sell most)
# - Pricing history for trend analysis
# - Revenue calculations by order, item, or time period
# - Customer purchasing pattern analysis
