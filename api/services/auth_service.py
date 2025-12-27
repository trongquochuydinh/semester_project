from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.models.user import User
from api.utils import create_access_token, verify_password

from api.schemas import LoginResponse, MessageResponse
from api.db.user_db import clear_login_session, establish_login_session, get_user_by_identifier as db_get_user_by_identifier
from api.utils import UserAlreadyLoggedInError

def login_user(identifier: str, password: str, db: Session) -> LoginResponse:
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

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        id=user.id,
        username=user.username,
        role=user.role.name,
        company_id=user.company_id
    )

def logout_user(current_user: User, db: Session) -> MessageResponse:
    clear_login_session(db, current_user)
    return MessageResponse(
        message="User logged out successfully"
    )

def verify_user(identifier: str, password: str, db):
    user = db_get_user_by_identifier(db, identifier)
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
