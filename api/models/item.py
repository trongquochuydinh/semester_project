from decimal import Decimal
from sqlalchemy import (
    String,
    Integer,
    Numeric,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.db_engine import Base


class Item(Base):
    """
    Item model for product catalog and inventory management.

    Represents products/services that can be ordered by customers.
    Includes pricing, inventory tracking, and company-based multi-tenant isolation.

    Features:
        - Product information (name, SKU)
        - Pricing with decimal precision for currency
        - Inventory quantity tracking
        - Active/inactive status for catalog management
        - Multi-tenant isolation by company
        - Order history through relationships

    Business Logic:
        - Items belong to one company (multi-tenant)
        - Can be active (available for orders) or inactive (hidden)
        - Inventory tracked through quantity field
        - Historical pricing preserved in order items
    """
    __tablename__ = "items"

    # --- Primary Key ---
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,               # Unique item identifier
    )

    # --- Product Information ---
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,                 # Product name/title
    )

    sku: Mapped[str] = mapped_column(
        String,
        nullable=False,                 # Stock Keeping Unit (product code)
    )

    # --- Pricing ---
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),                 # Decimal(10,2): up to 99,999,999.99
        nullable=False,                 # Current selling price
    )

    # --- Inventory Management ---
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,                      # Available inventory count
    )

    # --- Status Management ---
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,                   # True = available, False = hidden from catalog
    )

    # --- Multi-tenant Association ---
    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),  # Delete item if company deleted
        nullable=False,                 # Every item must belong to a company
    )

    # -------------------------
    # Relationships
    # -------------------------

    company = relationship(
        "Company",
        back_populates="items",         # Access company this item belongs to
    )

    order_items = relationship(
        "OrderItem",
        back_populates="item",          # Access all orders containing this item
        passive_deletes=True,           # Handle CASCADE delete efficiently
    )

# --- Item Management Design Notes ---
# Pricing Strategy:
# - Current price stored in item.price for catalog display
# - Historical prices preserved in OrderItem.unit_price for audit
# - Use Numeric type for exact decimal calculations (avoid float rounding)
#
# Inventory Tracking:
# - quantity field tracks available stock
# - Decremented when orders are fulfilled
# - Incremented when inventory is restocked
# - Consider implementing reorder points and low stock alerts
#
# Product Lifecycle:
# - is_active controls catalog visibility without deleting data
# - Inactive items hidden from new orders but preserved for history
# - SKU should be unique within company for inventory management
#
# Multi-tenant Considerations:
# - Items isolated by company_id for data security
# - Same SKU can exist across different companies
# - Pricing and inventory independent per company
#
# Order Integration:
# - Items can appear in multiple orders through OrderItem relationship
# - Price captured at order time preserves pricing history
# - Item deletion should consider existing order references
