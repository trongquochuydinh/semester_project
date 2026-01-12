"""
Database module initialization file.

This module provides centralized access to all database operation functions.
By importing all functions from item_db, we expose item-related database operations
at the package level for easier imports throughout the application.

Usage:
    from api.db import insert_item, get_item_data_by_id
    
    # Instead of:
    # from api.db.item_db import insert_item, get_item_data_by_id

Design Pattern: Namespace flattening for commonly used database functions.
"""

# Import all item database functions to package namespace
from api.db.item_db import *
from api.db.company_db import *
from api.db.order_items_db import *
from api.db.order_db import *
from api.db.user_db import *
from api.db.role_db import *
from api.db.oauth_db import *