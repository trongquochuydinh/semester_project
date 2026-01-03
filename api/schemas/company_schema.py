from pydantic import BaseModel
from typing import List

class CompanyOut(BaseModel):
    id: int
    name: str

class CompaniesResponse(BaseModel):
    companies: List[CompanyOut]

class CompanyCreate(BaseModel):
    name: str
    field: str