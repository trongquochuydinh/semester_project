from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.db_engine import Base


class Order(Base):
    """
    Order model for customer order management and lifecycle tracking.

    Represents customer orders with status tracking, timestamps, and associations
    to users and companies for multi-tenant order management.

    Features:
        - Order status workflow tracking
        - Order type categorization
        - Creation and completion timestamps
        - User association (who created the order)
        - Multi-tenant company isolation
        - Order items relationship for line items

    Order Lifecycle:
        created → processing → shipped → completed
        Alternative: created/processing → cancelled

    Multi-tenant Design:
        - Orders belong to specific company for data isolation
        - Users can only access orders within their company
        - Order fulfillment scoped by company context
    """

    __tablename__ = "orders"

    # --- Primary Key ---
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,               # Unique order identifier
    )

    # --- Order Status and Classification ---
    status: Mapped[str] = mapped_column(
        String,
        nullable=False,                 # Current order status (pending, processing, completed, etc.)
    )

    order_type: Mapped[str] = mapped_column(
        String,
        nullable=False,                 # Order classification (standard, rush, bulk, etc.)
    )

    # --- Timestamps ---
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,        # Auto-set creation timestamp
        nullable=False,
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,                  # Set when order is completed (null for pending orders)
    )

    # --- Associations ---
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),         # User who created/owns this order
        nullable=False,
    )

    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.id"),     # Company this order belongs to
        nullable=False,
    )

    # -------------------------
    # Relationships
    # -------------------------

    user = relationship(
        "User",
        back_populates="orders",        # Access user who created this order
    )

    company = relationship(
        "Company",
        back_populates="orders",        # Access company this order belongs to
    )

    items = relationship(
        "OrderItem",
        back_populates="order",         # Access all items in this order
        cascade="all, delete-orphan",   # Delete order items when order deleted
    )

# --- Order Management Design Notes ---
# Status Workflow:
# Common statuses: "created", "processing", "shipped", "completed", "cancelled"
# - created: Order placed but not yet processed
# - processing: Order being prepared/fulfilled
# - shipped: Order sent to customer
# - completed: Order delivered and finalized
# - cancelled: Order cancelled before completion
#
# Order Types:
# Examples: "standard", "rush", "bulk", "subscription", "return"
# - Used for different fulfillment processes
# - May affect pricing, priority, or shipping methods
# - Extensible for business-specific order categories
#
# Timestamp Strategy:
# - created_at: Always set for order tracking and reporting
# - completed_at: Set only when order reaches final status
# - Additional timestamps can be added (shipped_at, cancelled_at, etc.)
#
# Multi-tenant Security:
# - company_id ensures orders are isolated by organization
# - Users can only view/modify orders within their company
# - Cross-company order access requires superadmin privileges
#
# Business Intelligence:
# - Order timestamps enable reporting and analytics
# - Status tracking supports fulfillment metrics
# - User association enables sales tracking and commissions
# - Company association enables multi-tenant reporting
