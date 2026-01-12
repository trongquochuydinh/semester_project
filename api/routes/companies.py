from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import require_role, get_db
from api.models.user import User
from api.schemas import(
    CompanyCreateRequest,
    CompanyEditRequest,
    PaginationRequest
)

from api.services import (
    create_company, 
    get_info_of_company, 
    edit_company,
    delete_company,
    paginate_companies,
    list_companies
)

router = APIRouter(prefix="/api/companies", tags=["companies"])

@router.get("/get_companies")
def get_companies_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    """
    Get list of companies accessible to current user.
    
    Returns companies based on user's role and permissions:
    - Superadmins: See all companies in system
    - Admins/Managers: See only their own company
    
    Args:
        db: Database session for company queries
        current_user: Authenticated user for permission scoping
        
    Returns:
        list: Companies accessible to current user
        
    Used for: Company selection dropdowns, multi-tenant context switching,
             admin dashboards showing company information
    """
    return list_companies(db, current_user)

@router.get("/get/{company_id}")
def get_company_endpoint(
    company_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin"]))
):
    """
    Get detailed information for specific company.
    
    Returns complete company profile for viewing and editing.
    Restricted to superadmins only for security.
    
    Args:
        company_id: Unique identifier of company to retrieve
        db: Database session for company lookup
        current_user: Authenticated superadmin user
        
    Returns:
        dict: Company details including name, field, and metadata
        
    Authorization: Superadmin only - prevents unauthorized company data access
    Used for: Company detail pages, edit form pre-population, system administration
    """
    return get_info_of_company(company_id, db)

@router.post("/paginate")
def paginate_companies_endpoint(
    data: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin"])),
):
    """
    Get paginated list of all companies with filtering and search.
    
    Provides comprehensive company listing for system administration
    with support for filtering, sorting, and pagination.
    
    Args:
        data: Pagination parameters (page, size, filters, sort)
        db: Database session for company queries  
        current_user: Authenticated superadmin user
        
    Returns:
        PaginationResponse: Paginated company list with metadata
        
    Features:
        - Search by company name
        - Filter by business field/industry
        - Sort by various company attributes
        - Full system view for administrators
        
    Authorization: Superadmin only - prevents unauthorized system-wide access
    Used for: Company management interfaces, system administration dashboards
    """
    return paginate_companies(
        db=db,
        limit=data.limit,
        offset=data.offset,
        filters=data.filters
    )

# --- Company Management Endpoints (Superadmin Only) ---

@router.post("/create")
def create_company_endpoint(
    data: CompanyCreateRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin"]))
):
    """
    Create new company in the multi-tenant system.
    
    Establishes new tenant organization with unique name validation.
    Only superadmins can create companies to maintain system integrity.
    
    Args:
        data: Company creation data (name, field/industry)
        db: Database session for company creation
        current_user: Authenticated superadmin user
        
    Returns:
        dict: Success message and created company information
        
    Validation:
        - Company name must be unique across entire system
        - Required fields validated through Pydantic schema
        
    Authorization: Superadmin only - prevents unauthorized tenant creation
    Used for: System setup, new client onboarding, tenant provisioning
    """
    return create_company(data, db)

@router.post("/edit/{company_id}")
def edit_company_endpoint(
    company_id: int, 
    data: CompanyEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin"]))
):
    """
    Update existing company information.
    
    Allows modification of company details with validation for uniqueness
    and business rules. Changes may affect all users within the company.
    
    Args:
        company_id: ID of company to update
        data: Updated company information
        db: Database session for company updates
        current_user: Authenticated superadmin user
        
    Returns:
        dict: Update confirmation message
        
    Validation:
        - Company name uniqueness (excluding current company)
        - Field updates validated through schema
        
    Authorization: Superadmin only - prevents unauthorized tenant modification
    Impact: May affect company display names throughout system
    """
    return edit_company(company_id, db, data)

@router.post("/delete/{company_id}")
def delete_company_endpoint(
    company_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin"]))
):
    """
    Delete company and all associated data from system.
    
    Performs hard delete of company and cascades to all related data:
    users, items, orders, and other company-scoped entities.
    
    Args:
        company_id: ID of company to delete
        db: Database session for deletion operations
        current_user: Authenticated superadmin user
        
    Returns:
        dict: Deletion confirmation message
        
    WARNING: This is a destructive operation that:
        - Permanently deletes company and all related data
        - Cannot be undone without database backups
        - Affects all users, orders, and items in the company
        
    Authorization: Superadmin only - prevents accidental data loss
    Used for: Tenant offboarding, system cleanup, contract terminations
    
    Consider: Implement soft delete in production for safety
    """
    return delete_company(company_id, db)
