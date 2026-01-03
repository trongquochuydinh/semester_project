from fastapi import HTTPException
from requests import Session
from sqlalchemy.orm import Session

from api.schemas import CompaniesResponse, CompanyOut, MessageResponse

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

from api.utils import normalize_string

def create_company(data, db: Session):
    existing = db_company_exists_by_name(db, data.name.strip().lower())
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Company with this name already exists"
        )

    company = Company(
        name=data.name,
        field=data.field
    )

    db_create_company(db, company)

    return {
        "message": "Company created successfully",
        "company_id": company.id
    }

def edit_company(company_id: int, db: Session, data) -> MessageResponse:

    company = db_get_company_data_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    if db_company_exists_by_name_excluding_id(
        db=db,
        name=normalize_string(data.get("name").lower(), "name"),
        exclude_company_id=company_id,
    ):
        raise HTTPException(
            status_code=400,
            detail="Company with this name already exists"
        )

    updates = {
        "name": data.get("name").strip(),
        "field": data.get("field"),
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
    company = db_get_company_data_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db_delete_company(db, company)

    return MessageResponse(
        message="Company was successfully deleted."
    )

def get_info_of_company(company_id, db):
    company = db_get_company_data_by_id(db, company_id)
    company_dict = {
        "id" : company.id,
        "company_name" : company.name,
        "field" : company.field 
    }
    return company_dict

def list_companies(db: Session, current_user: User):
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
    if is_superadmin:
        return

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
    company_id: int,
) -> Company:
    company = db_get_company_data_by_id(db, company_id)

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

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
    query = db.query(Company)

    for key, value in filters.items():
        if hasattr(Company, key):
            query = query.filter(getattr(Company, key) == value)

    total = query.count()
    results = query.offset(offset).limit(limit).all()

    def to_dict(obj):
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

    data = [to_dict(r) for r in results]
    return {"total": total, "data": data}