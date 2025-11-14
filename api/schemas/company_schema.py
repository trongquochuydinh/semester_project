from pydantic import BaseModel

class CompanyCreate(BaseModel):
    company_name: str
    field: str