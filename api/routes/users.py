from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from api.db.db_engine import get_db
from api.models.user import User
from api.schemas.user_schema import (
    LoginRequest, UserResponse, UserCreate, RolesResponse, LogoutRequest, RoleOut
)
from api.services import (
    login_user, get_subroles_for_role, create_user_account, logout_user, get_current_user, require_role, get_user_count, get_info_of_user
)

router = APIRouter(prefix="/api/users", tags=["users"])
security = HTTPBearer()

@router.post("/login", response_model=UserResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(data.identifier, data.password, db)

@router.get("/get_subroles", response_model=RolesResponse)
def get_subroles(creator_role: str = Query(...), db: Session = Depends(get_db)):
    roles = get_subroles_for_role(creator_role)
    return RolesResponse(roles=[RoleOut(name=name) for name in roles])

@router.post("/create")
def create_user_endpoint(data: UserCreate, db: Session = Depends(get_db)):
    return create_user_account(data, db)

@router.post("/logout")
def logout(data: LogoutRequest, db: Session = Depends(get_db)):
    return logout_user(data.user_id, db)

@router.get("/me")
def get_me(token=Depends(security), db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.roles[0].role.name if current_user.roles else None,
    }

@router.get("/get/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_info_of_user(user_id, db)

@router.get("/get_my_role")
def get_my_role(token=Depends(security), db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    return {"role": current_user.roles[0].role.name if current_user.roles else None}

@router.get("/get_user_stats")
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    role_name = (
        current_user.roles[0].role.name
        if current_user.roles and current_user.roles[0].role
        else None
    )

    if role_name == "superadmin":
        total = get_user_count(db)
        online = get_user_count(db, online_only=True)
    elif role_name == "admin":
        if not current_user.company_id:
            raise HTTPException(status_code=400, detail="Admin user is not assigned to any company")
        total = get_user_count(db, company_id=current_user.company_id)
        online = get_user_count(db, company_id=current_user.company_id, online_only=True)
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")

    return {"total_users": total, "online_users": online}