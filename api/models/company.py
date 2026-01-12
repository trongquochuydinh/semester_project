# Import SQLAlchemy components for ORM model definition
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Import database base class for model inheritance
from api.db.db_engine import Base


class Company(Base):
    """
    Company model for multi-tenant organization management.

    Serves as the primary tenant container that isolates data between different
    organizations using the system. All business data (users, items, orders)
    is scoped by company to ensure data privacy and security.

    Features:
        - Multi-tenant data isolation
        - Unique company identification
        - Business categorization by field/industry
        - Cascading relationships for data integrity

    Multi-tenant Design:
        - Each company operates as an isolated tenant
        - Users belong to one company and can only access that company's data
        - All business entities (items, orders) are company-scoped
        - Superadmins can access cross-company data for system management
    """
    __tablename__ = "companies"

    # --- Primary Key ---
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,               # Unique company identifier
    )

    # --- Company Information ---
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,                    # Enforce unique company names globally
    )

    field: Mapped[str] = mapped_column(
        String,
        nullable=True,                  # Business field/industry (optional)
    )

    # -------------------------
    # Relationships
    # -------------------------

    users = relationship(
        "User",
        back_populates="company",       # All users belonging to this company
        cascade="all, delete-orphan",   # Delete users when company is deleted
    )

    items = relationship(
        "Item",
        back_populates="company",       # All products/inventory for this company
        cascade="all, delete-orphan",   # Delete items when company is deleted
    )

    orders = relationship(
        "Order",
        back_populates="company",       # All orders placed within this company
        cascade="all, delete-orphan",   # Delete orders when company is deleted
    )

# --- Multi-tenant Architecture Notes ---
# Data Isolation:
# - All business data filtered by company_id in queries
# - Users can only access data within their assigned company
# - Cross-company data access prevented at database query level
#
# Cascade Behavior:
# - Deleting company removes all related data (users, items, orders)
# - Ensures complete cleanup when removing tenants
# - Use with extreme caution - consider soft delete in production
#
# Security Considerations:
# - Company name uniqueness prevents confusion
# - All API endpoints should validate company_id against user's company
# - Superadmin role needed for cross-company operations
#
# Business Use Cases:
# - SaaS application serving multiple organizations
# - Corporate system with different departments/divisions
# - Marketplace with multiple vendor companies
# - Any system requiring data segregation by organization
