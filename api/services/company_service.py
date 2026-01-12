from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.schemas import CompaniesResponse, CompanyOut, MessageResponse, CompanyCreateRequest, CompanyEditRequest

from api.models import User, Company
from api.db.company_db import (
    get_company_data_by_id as db_get_company_data_by_id,
    create_company as db_create_company,
    edit_company as db_edit_company,
    company_exists_by_name_excluding_id as db_company_exists_by_name_excluding_id,
    delete_company as db_delete_company,
    company_exists_by_name as db_company_exists_by_name,
    list_companies as db_list_companies
)

from api.utils import normalize_string, validate_company_data

def create_company(data: CompanyCreateRequest, db: Session) -> MessageResponse:
    """Create new company with uniqueness validation."""
    validate_company_data(data)

    # Check for duplicate company name
    existing = db_company_exists_by_name(db, data.name.strip().lower())
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Company with this name already exists"
        )

    # Create company object
    company = Company(
        name=data.name,
        field=data.field
    )

    db_create_company(db, company)

    return MessageResponse(
        message="Company created successfully."
    )

def edit_company(company_id: int, db: Session, data: CompanyEditRequest) -> MessageResponse:
    """Update company with uniqueness validation."""
    validate_company_data(data)
    
    company = db_get_company_data_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Check for name conflicts excluding current company
    if db_company_exists_by_name_excluding_id(
        db=db,
        name=normalize_string(data.name.lower(), "name"),
        exclude_company_id=company_id,
    ):
        raise HTTPException(
            status_code=409,
            detail="Company with this name already exists"
        )

    # Build update data
    updates = {
        "name": data.name.strip(),
        "field": data.field,
    }

    db_edit_company(
        db=db,
        company=company,
        updates=updates
    )

    return MessageResponse(
        message="Company was successfully updated."
    )

def delete_company(company_id: int, db: Session) -> MessageResponse:
    """Delete company and all related data."""
    company = db_get_company_data_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_delete_company(db, company)

    return MessageResponse(
        message="Company was successfully deleted."
    )

def get_info_of_company(company_id, db):
    """Get company details by ID."""
    company = db_get_company_data_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company_dict = {
        "id" : company.id,
        "company_name" : company.name,
        "field" : company.field 
    }
    return company_dict

def list_companies(db: Session, current_user: User):
    """Get companies based on user permissions."""
    companies = db_list_companies(
        db=db,
        is_superadmin=current_user.role.name == "superadmin",
        user_company_id=current_user.company_id,
    )

    return CompaniesResponse(
        companies=[
            CompanyOut(id=c.id, name=c.name)
            for c in companies
        ]
    )

def assert_user_company_scope(
    *,
    is_superadmin: bool,
    current_user_company_id: int,
    target_company_id: int,
):
    """Validate user can access target company."""
    if is_superadmin:
        return  # Superadmins have global access

    if current_user_company_id != target_company_id:
        raise HTTPException(
            status_code=403,
            detail="Operation not allowed outside your company",
        )

def assert_company_access(
    db: Session,
    *,
    is_superadmin: bool,
    current_user_company_id: int,
    company_id: Optional[int],
) -> Company:
    """Validate and return company with access control."""
    company = db_get_company_data_by_id(db, company_id)

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    # Check if user can access this company
    assert_user_company_scope(
        is_superadmin=is_superadmin,
        current_user_company_id=current_user_company_id,
        target_company_id=company.id,
    )

    return company

def paginate_companies(
    db: Session,
    limit: int,
    offset: int,
    filters: dict
):
    """Get paginated company list with filtering."""
    query = db.query(Company)

    # Apply filters
    for key, value in filters.items():
        if hasattr(Company, key):
            query = query.filter(getattr(Company, key) == value)

    total = query.count()
    results = query.offset(offset).limit(limit).all()

    def to_dict(obj):
        """Convert company to dictionary."""
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

    data = [to_dict(r) for r in results]
    return {"total": total, "data": data}