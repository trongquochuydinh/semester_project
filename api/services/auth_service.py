from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.models.user import User
from api.services import verify_user
from api.utils import create_access_token

from api.schemas.user_schema import UserResponse
from api.db.user_db import change_user_status

def login_user(identifier: str, password: str, db: Session) -> UserResponse:
    user = verify_user(identifier, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    change_user_status(db, user, "online")

    token = create_access_token(user.id, user.role.name)

    user_response = UserResponse(
        access_token=token,
        token_type="bearer",
        id=user.id,
        username=user.username,
        role=user.role.name,
        company_id=user.company_id
    )

    return user_response

def logout_user(current_user: User, db: Session):
    change_user_status(db, current_user, "offline")
    return {"message": "User logged out successfully"}
