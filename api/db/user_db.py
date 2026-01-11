import uuid
from sqlalchemy import or_, false
from sqlalchemy.orm import Session, joinedload
from api.models.user import User
from api.models.role import Role
from api.models.oauth import UserOAuthAccount
from datetime import datetime
from typing import List, Optional, Set

from api.utils import UserAlreadyLoggedInError

def insert_user(db: Session, user: User):
    db.add(user)
    db.flush()

def user_exists_by_username_or_email(
    db: Session,
    *,
    username: str,
    email: str,
    exclude_user_id: Optional[int]
) -> bool:
    query = db.query(User).filter(
        or_(
            User.username == username,
            User.email == email,
        )
    )

    if exclude_user_id is not None:
        query = query.filter(User.id != exclude_user_id)

    return query.first() is not None

def edit_user(
    db: Session,
    user: User,
    updates: dict,
    role_id: int,
) -> User:

    EDITABLE_FIELDS = {
        "username",
        "email",
        "company_id"
    }

    for key, value in updates.items():
        if key in EDITABLE_FIELDS:
            setattr(user, key, value)

    # Apply role update explicitly
    user.role_id = role_id

    db.flush()
    db.refresh(user)
    return user

def change_user_status(user: User, status: str):
    user.status = status
    if status == "online":
        user.last_login = datetime.now()
    
def change_user_is_active(db: Session, user: User, is_active: bool):
    user.is_active = is_active
    clear_login_session(user)
    db.flush()
    db.refresh(user)

def establish_login_session(user: User) -> str:
    if user.session_id is not None:
        raise UserAlreadyLoggedInError()

    session_id = str(uuid.uuid4())
    user.session_id = session_id
    change_user_status(user, "online")
    return session_id

def clear_login_session(user: User):
    user.session_id = None
    change_user_status(user, "offline")

def clear_login_session_by_user_id(db: Session, user_id: int):
    user = get_user_data_by_id(db, user_id)
    if user:
        clear_login_session(user)
        db.commit() 

def get_user_data_by_id(db: Session, user_id: int) -> Optional[User]:
    return (
        db.query(User)
        .options(
            joinedload(User.role),
            joinedload(User.company),
        )
        .filter(User.id == user_id)
        .first()
    )

def get_user_by_identifier(db: Session, identifier: str) -> Optional[User]:
    return (
        db.query(User)
        .options(
            joinedload(User.role),
            joinedload(User.company),
        )
        .filter(
            (User.username == identifier) |
            (User.email == identifier)
        )
        .first()
    )

def get_oauth_providers(db: Session, user_id: int) -> Set[str]:
    rows = (
        db.query(UserOAuthAccount.provider)
        .filter(UserOAuthAccount.user_id == user_id)
        .all()
    )
    return {row.provider for row in rows}

def paginate_users(
    db: Session,
    filters: dict,
    allowed_roles: Optional[Set[str]],
    company_id: int,
    limit: int,
    offset: int,
):
    query = (
        db.query(User)
        .options(
            joinedload(User.role),
            joinedload(User.company),
        )
    )

    # Apply filters
    for key, value in filters.items():
        if hasattr(User, key):
            query = query.filter(getattr(User, key) == value)

    # Role restriction
    if allowed_roles is not None:
        if allowed_roles:
            query = (
                query
                .join(User.role)
                .filter(Role.name.in_(allowed_roles))
            )
        else:
            query = query.filter(false())

    # Company restriction
    if company_id is not None:
        query = query.filter(User.company_id == company_id)

    total = query.count()
    results = query.offset(offset).limit(limit).all()

    return total, results

def count_users(db: Session, company_id=None, online_only=False):
    query = db.query(User)
    if company_id is not None:
        query = query.filter(User.company_id == company_id)
    if online_only:
        query = query.filter(User.status == "online")
    return query.count()
