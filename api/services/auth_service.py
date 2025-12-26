from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.models.user import User
from api.services import verify_user
from api.utils import create_access_token

from api.schemas.user_schema import UserResponse
from api.db.user_db import clear_login_session, establish_login_session
from api.utils import UserAlreadyLoggedInError

def login_user(identifier: str, password: str, db: Session) -> UserResponse:
    user = verify_user(identifier, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        session_id = establish_login_session(db, user)
    except UserAlreadyLoggedInError:
        raise HTTPException(
            status_code=409,
            detail="User is already logged in elsewhere"
        )

    token = create_access_token(
        user.id,
        user.role.name,
        session_id=session_id
    )

    return UserResponse(
        access_token=token,
        token_type="bearer",
        id=user.id,
        username=user.username,
        role=user.role.name,
        company_id=user.company_id
    )

def logout_user(current_user: User, db: Session):
    clear_login_session(db, current_user)
    return {"message": "User logged out successfully"}
