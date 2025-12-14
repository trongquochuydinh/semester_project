from requests import Session
from sqlalchemy.orm import Session

from api.models.company import Company
from api.db.company_db import get_company_data_by_id as db_get_company_data_by_id

def create_company(data, db: Session):
    company = Company(
        name=data.company_name,
        field=data.field
    )
    db.add(company)
    db.commit()
    db.refresh(company)

    return {"message": "Company created successfully", "company_id": company.id}

def get_info_of_company(company_id, db):
    company = db_get_company_data_by_id(db, company_id)
    company_dict = {
        "id" : company.id,
        "company_name" : company.name,
        "field" : company.field 
    }
    return company_dict