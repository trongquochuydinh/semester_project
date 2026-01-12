# Import SQLAlchemy ORM components for database operations
from sqlalchemy.orm import Session

# Import Role model for database table interaction
from api.models.role import Role

def get_role_by_id(db: Session, role_id: int):
    """
    Retrieve a specific role by its unique identifier.
    
    Args:
        db (Session): Database session for query execution
        role_id (int): Unique identifier of the role to retrieve
        
    Returns:
        Role: Role object if found, None otherwise
        
    Used for: Role validation, user role assignment, permission checking
    """
    return db.query(Role).filter_by(id=role_id).first()

def get_role_by_name(db: Session, role_name: str):
    """
    Find a role by its name (case-sensitive lookup).
    
    Args:
        db (Session): Database session
        role_name (str): Name of the role to find (e.g., 'admin', 'user', 'manager')
        
    Returns:
        Role: Role object if found, None otherwise
        
    Used for: Role-based access control, authorization checks, role validation
    """
    return db.query(Role).filter(Role.name == role_name).first()

def get_all_roles(db: Session):
    """
    Retrieve all available roles in the system.
    
    Args:
        db (Session): Database session
        
    Returns:
        List[Role]: List of all role objects in the database
        
    Used for: Role selection dropdowns, admin interfaces, system setup
    Note: Returns all roles regardless of permissions - filter at application level
    """
    return db.query(Role).all()

# --- Role System Design Notes ---
# Roles define permission levels and access rights throughout the application
# Common role hierarchy: superadmin > admin > manager > user
# Role names should be consistent and descriptive for clear authorization logic
# Consider caching role data since it changes infrequently
