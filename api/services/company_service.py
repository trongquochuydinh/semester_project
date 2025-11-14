from requests import Session
from sqlalchemy.orm import Session

from api.models.company import Company

def create_company(data, db: Session):
    company = Company(
        name=data.company_name,
        field=data.field
    )
    db.add(company)
    db.commit()
    db.refresh(company)

    return {"message": "Company created successfully", "company_id": company.id}