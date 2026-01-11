from pydantic import BaseModel
from typing import List

class CompanyOut(BaseModel):
    id: int
    name: str

class CompaniesResponse(BaseModel):
    companies: List[CompanyOut]

class CompanyWriter(BaseModel):
    name: str
    field: str

class CompanyCreateRequest(CompanyWriter):
    pass

class CompanyEditRequest(CompanyWriter):
    pass