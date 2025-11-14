import secrets
import string
from typing import Dict
from fastapi import Depends, HTTPException
from requests import Session
from sqlalchemy.orm import Session, joinedload
from werkzeug.security import generate_password_hash

from api.db.db_engine import SessionLocal, get_db
from api.models.company import Company

def create_company(data, db: Session = Depends(get_db)):
    try:

        user = Company(
            name=data.company_name,
            field=data.field
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        db.commit()
        return {"message": "Company created successfully"}
    finally:
        db.close()