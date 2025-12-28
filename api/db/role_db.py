from sqlalchemy.orm import Session
from api.models.role import Role

def get_role_by_id(db: Session, role_id: int):
    return db.query(Role).filter_by(id=role_id).first()

def get_role_by_name(db: Session, role_name: str):
    return db.query(Role).filter(Role.name == role_name).first()

def get_all_roles(db: Session):
    return db.query(Role).all()
