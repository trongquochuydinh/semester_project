from sqlalchemy.orm import Session, joinedload
from api.models.user import User, UserRole, Role


def insert_user(db: Session, user: User) -> User:
    db.add(user)
    db.flush()      # assigns user.id
    return user

def get_role_by_id(db: Session, role_id: int):
    return db.query(Role).filter_by(id=role_id).first()

def get_id_by_role(db: Session, role):
    return db.query(Role).filter(Role.name == role).first()

def get_all_roles(db: Session):
    return db.query(Role).all()

def get_user_data_by_id(db: Session, user_id: int) -> User:
    return (
        db.query(User)
        .options(joinedload(User.roles).joinedload(UserRole.role))
        .filter(User.id == user_id)
        .first()
    )

def assign_role(db: Session, user_id: int, role_id: int):
    db.add(UserRole(user_id=user_id, role_id=role_id))
    db.flush()

def get_user_by_identifier(db: Session, identifier: str) -> User:
    return (
        db.query(User)
        .options(joinedload(User.roles).joinedload(UserRole.role))
        .filter((User.username == identifier) | (User.email == identifier))
        .first()
    )


def paginate_users(db: Session, filters, allowed_roles, company_id, limit, offset):
    query = (
        db.query(User)
        .options(
            joinedload(User.roles).joinedload(UserRole.role),
            joinedload(User.company)
        )
    )

    # Apply filters
    for key, value in filters.items():
        if hasattr(User, key):
            query = query.filter(getattr(User, key) == value)

    # Role restrictions
    if allowed_roles:
        query = query.join(UserRole).join(Role).filter(Role.name.in_(allowed_roles))
    elif allowed_roles == []:
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
