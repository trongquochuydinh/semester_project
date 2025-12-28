import uuid
from sqlalchemy.orm import Session, joinedload
from api.models.user import User
from api.models.role import Role
from datetime import datetime
from typing import List

from api.utils import UserAlreadyLoggedInError

def insert_user(db: Session, user: User) -> User:
    db.add(user)
    db.flush()

def edit_user(
    db: Session,
    user_id: int,
    updates: dict,
    role_id: int,
) -> User:

    EDITABLE_FIELDS = {
        "username",
        "email",
        "status",
    }

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    for key, value in updates.items():
        if key in EDITABLE_FIELDS:
            setattr(user, key, value)

    # Apply role update explicitly
    user.role_id = role_id

    db.flush()
    return user

def change_user_status(db: Session, user: User, status: str):
    user.status = status
    if status == "online":
        user.last_login = datetime.now()
    
def establish_login_session(db: Session, user: User) -> str:
    if user.session_id is not None:
        raise UserAlreadyLoggedInError()

    session_id = str(uuid.uuid4())
    user.session_id = session_id
    change_user_status(db, user, "online")
    return session_id

def clear_login_session(db: Session, user: User):
    user.session_id = None
    change_user_status(db, user, "offline")

def clear_login_session_by_user_id(db: Session, user_id: int):
    user = get_user_data_by_id(db, user_id)
    if user:
        clear_login_session(db, user)

def get_user_data_by_id(db: Session, user_id: int) -> User:
    return (
        db.query(User)
        .options(
            joinedload(User.role),
            joinedload(User.company),
        )
        .filter(User.id == user_id)
        .first()
    )

def get_user_by_identifier(db: Session, identifier: str) -> User:
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

def paginate_users(
    db: Session,
    filters: dict,
    allowed_roles: List[str],
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
            # Explicitly no allowed roles
            query = query.filter(False)

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
