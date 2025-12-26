from sqlalchemy.orm import Session
from api.models.company import Company

def get_company_data_by_id(db: Session, company_id: int) -> Company:
    return (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )