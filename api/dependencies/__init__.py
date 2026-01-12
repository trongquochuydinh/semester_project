"""
Dependencies module initialization file.

This module provides centralized access to all FastAPI dependency functions
by importing and exposing authentication and database dependencies at the package level.

Available Dependencies:
    From auth.py:
        - get_current_user: Extract and validate authenticated user from JWT token
        - require_role: Role-based access control decorator factory
        
    From db.py:
        - get_db: Database session dependency with transaction management

Usage:
    from api.dependencies import get_current_user, get_db, require_role
    
    @router.get("/protected")
    def protected_route(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        return {"user_id": user.id}

Design Pattern: Namespace flattening for commonly used dependency functions.
"""

# Import all authentication dependencies to package namespace
from api.dependencies.auth import *

# Import all database dependencies to package namespace  
from api.dependencies.db import *

# --- Dependency Injection Benefits ---
# FastAPI's dependency injection system provides:
# - Automatic parameter resolution and injection
# - Request-scoped database sessions with proper cleanup
# - Reusable authentication and authorization logic
# - Clean separation of concerns between routes and business logic
# - Automatic OpenAPI documentation generation for security schemes