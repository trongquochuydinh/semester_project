from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

from requests import Session
from api.db.db_engine import SessionLocal, get_db
from api.models.company import Company
from api.schemas.company_schema import CompanyCreate

from api.services import create_company

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