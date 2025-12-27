from requests import Session
from sqlalchemy.orm import Session

from api.models.company import Company
from api.db.company_db import get_company_data_by_id as db_get_company_data_by_id

# TODO: Move db logic somewhere else
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

def paginate_companies(
    db: Session,
    limit: int,
    offset: int,
    filters: dict
):
    query = db.query(Company)

    for key, value in filters.items():
        if hasattr(Company, key):
            query = query.filter(getattr(Company, key) == value)

    total = query.count()
    results = query.offset(offset).limit(limit).all()

    def to_dict(obj):
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

    data = [to_dict(r) for r in results]
    return {"total": total, "data": data}