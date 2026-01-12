"""
Models package initialization file.

This module provides centralized access to all SQLAlchemy ORM models by importing
and exposing them at the package level for consistent usage throughout the application.

Available Models:
    - User: User accounts with authentication and role-based access
    - Company: Multi-tenant organization containers
    - Role: Permission levels and access rights
    - Item: Product catalog and inventory management
    - Order: Customer orders and order lifecycle
    - OrderItem: Individual items within orders with pricing
    - UserOAuthAccount: External authentication provider linkage

Usage:
    from api.models import User, Company, Order
    
    # Instead of:
    # from api.models.user import User
    # from api.models.company import Company
    # from api.models.order import Order

Database Design: Multi-tenant architecture with company-based data isolation
"""

# Import core user and authentication models
from api.models.user import User                    # User accounts and authentication
from api.models.role import Role                    # Role-based access control
from api.models.oauth import UserOAuthAccount       # OAuth provider integration

# Import multi-tenant organization model
from api.models.company import Company              # Tenant/organization containers

# Import business domain models
from api.models.item import Item                    # Product catalog and inventory
from api.models.order import Order                  # Customer orders
from api.models.order_item import OrderItem         # Order line items with pricing
