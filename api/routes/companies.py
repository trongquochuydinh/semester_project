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

from api.services import create_company, get_info_of_company, paginate_companies

router = APIRouter(prefix="/api/companies", tags=["companies"])

class CompanyResponse(BaseModel):
    id: int
    name: str

@router.get("/get_companies", response_model=List[CompanyResponse])
def get_companies():
    session = SessionLocal()
    try:
        companies = session.query(Company).all()
        return [CompanyResponse(id=company.id, name=company.name) for company in companies]
    finally:
        session.close()

@router.post("/create")
def create_company_endpoint(data: CompanyCreate, db: Session = Depends(get_db)):
    return create_company(data, db)

@router.get("/get/{company_id}")
def get_company(company_id, db: Session = Depends(get_db)):
    return get_info_of_company(company_id, db)

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
