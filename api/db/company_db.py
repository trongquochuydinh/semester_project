from sqlalchemy.orm import Session
from sqlalchemy import func
from api.models.company import Company

def get_company_data_by_id(db: Session, company_id: int) -> Company:
    return (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

def company_exists_by_name_excluding_id(
    db: Session,
    name: str,
    exclude_company_id: int,
) -> Company:
    return (
        db.query(Company)
        .filter(
            func.lower(func.trim(Company.name)) == name,
            Company.id != exclude_company_id
        )
        .first()
    )

def edit_company(
    db: Session,
    company: Company,
    updates: dict
):
    
    EDITABLE_FIELDS = {
        "name",
        "field",
    }

    for key, value in updates.items():
        if key in EDITABLE_FIELDS:
            setattr(company, key, value)

    db.flush()

    return company

def list_companies(
    db: Session,
    is_superadmin: bool,
    user_company_id: int = None,
):
    query = db.query(Company)

    if not is_superadmin:
        query = query.filter(Company.id == user_company_id)

    return query.all()

def create_company(db: Session, company: Company):
    db.add(company)
    db.flush()
    return

def delete_company(db: Session, company: Company):
    db.delete(company)

def company_exists_by_name(db: Session, name: str):
    return (
        db.query(Company)
        .filter(func.lower(func.trim(Company.name)) == name)
        .first()
    )