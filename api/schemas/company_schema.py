from pydantic import BaseModel
from typing import List, Optional

class CompanyOut(BaseModel):
    id: int
    name: str

class CompanyDetailResponse(BaseModel):
    id: int
    name: str
    field: Optional[str] = None

class CompaniesResponse(BaseModel):
    companies: List[CompanyOut]

class CompanyWriter(BaseModel):
    name: str
    field: str

class CompanyCreateRequest(CompanyWriter):
    pass

class CompanyEditRequest(CompanyWriter):
    pass
