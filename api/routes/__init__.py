"""
Routes package initialization file.

This package contains all FastAPI route definitions organized by business domain.
Each module defines API endpoints for a specific area of functionality with
consistent patterns for authentication, authorization, and error handling.

Route Modules:
    - users.py: User management, authentication, and profile operations
    - companies.py: Multi-tenant company management (superadmin only)
    - items.py: Product catalog and inventory management
    - orders.py: Order processing and lifecycle management

Common Patterns:
    - Dependency injection for database sessions and authentication
    - Role-based access control using require_role decorators
    - Consistent request/response schemas with Pydantic models
    - Multi-tenant data isolation through company_id filtering
    - Standardized error handling and HTTP status codes

Design Principles:
    - RESTful endpoint design with clear resource naming
    - Separation of concerns: routes handle HTTP, services handle business logic
    - Authentication required for all endpoints (except login/OAuth)
    - Authorization enforced at route level based on user roles
    - Automatic OpenAPI documentation generation for all endpoints
"""

# Note: This file is intentionally minimal as route registration happens in main.py
# Each route module exports a router that gets included in the main FastAPI app