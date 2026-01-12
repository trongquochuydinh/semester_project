from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from api.models.company import Company

def get_company_data_by_id(db: Session, company_id: Optional[int]) -> Optional[Company]:
    """
    Retrieve company information by unique identifier.
    
    Args:
        db (Session): Database session for query execution
        company_id (Optional[int]): Company ID to look up, None returns None
        
    Returns:
        Optional[Company]: Company object if found, None if not found or ID is None
        
    Used for: Company validation, multi-tenant context setup, company detail views
    """
    return (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

def company_exists_by_name_excluding_id(
    db: Session,
    name: str,
    exclude_company_id: int,
) -> Optional[Company]:
    """
    Check if company name already exists, excluding a specific company ID.
    
    Args:
        db (Session): Database session
        name (str): Company name to check (case-insensitive, whitespace-trimmed)
        exclude_company_id (int): Company ID to exclude from check (for updates)
        
    Returns:
        Optional[Company]: Existing company with same name, or None if unique
        
    Used for: Company name validation during edits, preventing duplicate names
    Security: Ensures company name uniqueness across the system
    """
    return (
        db.query(Company)
        .filter(
            func.lower(func.trim(Company.name)) == name,  # Case-insensitive comparison
            Company.id != exclude_company_id              # Exclude current company
        )
        .first()
    )

def edit_company(
    db: Session,
    company: Company,
    updates: dict
):
    """
    Update existing company information with field validation.
    
    Args:
        db (Session): Database session
        company (Company): Company object to update
        updates (dict): Dictionary of fields to update
        
    Returns:
        Company: Updated company object
        
    Security: Only allows updates to predefined safe fields
    """
    # Define which fields can be safely updated
    EDITABLE_FIELDS = {
        "name",   # Company name/title
        "field",  # Business field/industry
    }

    # Apply validated field updates
    for key, value in updates.items():
        if key in EDITABLE_FIELDS:
            setattr(company, key, value)

    # Persist changes to database
    db.flush()

    return company

def list_companies(
    db: Session,
    is_superadmin: bool,
    user_company_id: Optional[int] = None,
) -> List[Company]:
    """
    Get list of companies based on user permissions.
    
    Args:
        db (Session): Database session
        is_superadmin (bool): Whether user has superadmin privileges
        user_company_id (Optional[int]): User's company ID for regular users
        
    Returns:
        List[Company]: List of companies user is authorized to see
        
    Access Control:
        - Superadmins: See all companies
        - Regular users: See only their own company
        
    Used for: Company selection dropdowns, admin interfaces, reporting
    """
    query = db.query(Company)

    # Apply access control based on user permissions
    if not is_superadmin:
        # Regular users can only see their own company
        query = query.filter(Company.id == user_company_id)

    return query.all()

def create_company(db: Session, company: Company):
    """
    Create a new company in the system.
    
    Args:
        db (Session): Database session
        company (Company): Company object with all required fields populated
        
    Used for: System setup, new tenant onboarding, company registration
    Note: Uses flush() to get company ID for immediate use
    """
    db.add(company)
    db.flush()  # Persist to get company.id without committing transaction
    return

def delete_company(db: Session, company: Company):
    """
    Remove company from the system (hard delete).
    
    Args:
        db (Session): Database session
        company (Company): Company object to delete
        
    Warning: This is a hard delete that may affect related data.
    Ensure proper cascade handling and data backup before deletion.
    
    Used for: System cleanup, tenant offboarding, data management
    """
    db.delete(company)
    db.flush()  # Execute deletion immediately

def company_exists_by_name(db: Session, name: str):
    """
    Check if a company with the given name already exists.
    
    Args:
        db (Session): Database session
        name (str): Company name to check (case-insensitive, whitespace-trimmed)
        
    Returns:
        Company: Existing company if found, None otherwise
        
    Used for: Company creation validation, duplicate prevention
    """
    return (
        db.query(Company)
        .filter(func.lower(func.trim(Company.name)) == name)
        .first()
    )

# --- Multi-Tenant Company Design Notes ---
# Companies serve as top-level tenant containers for data isolation
# Company names must be unique across the entire system
# Access control enforced at query level based on user permissions
# Superadmins have cross-company access for system administration
# Regular users restricted to their own company's data
# Case-insensitive name matching prevents accidental duplicates