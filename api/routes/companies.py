from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from api.db.db_engine import SessionLocal
from api.models.company import Company

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