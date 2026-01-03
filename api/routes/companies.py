from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

from requests import Session
from api.db.db_engine import SessionLocal
from api.dependencies import require_role, get_db
from api.models.company import Company
from api.models.user import User
from api.schemas import(
    CompanyCreate,
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
    return list_companies(db, current_user)

@router.post("/create")
def create_company_endpoint(
    data: CompanyCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin"]))
):
    return create_company(data, db)

@router.get("/get/{company_id}")
def get_company_endpoint(
    company_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin"]))
):
    return get_info_of_company(company_id, db)

@router.post("/edit/{company_id}")
def edit_company_endpoint(
    company_id: int, 
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin"]))
):
    return edit_company(company_id, db, data)

@router.post("/delete/{company_id}")
def delete_company_endpoint(
    company_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin"]))
):
    return delete_company(company_id, db)

@router.post("/paginate")
def paginate_companies_endpoint(
    data: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin"])),
):
    return paginate_companies(
        db=db,
        limit=data.limit,
        offset=data.offset,
        filters=data.filters
    )
