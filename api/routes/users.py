from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, require_role
from api.db.db_engine import get_db
from api.models.user import User
from api.schemas import (
    LoginRequest, UserResponse, UserWriter, RolesResponse, RoleOut, MessageResponse
)
from api.services import (
    login_user, 
    get_subroles_for_role, 
    create_user_account, 
    logout_user,  
    get_user_count, 
    get_info_of_user,
    edit_user
)

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/login", response_model=UserResponse)
def login_user_endpoint(
    data: LoginRequest, 
    db: Session = Depends(get_db)
):
    return login_user(data.identifier, data.password, db)

@router.post("/logout", response_model=MessageResponse)
def logout_user_endpoint( 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return logout_user(current_user, db)

@router.get("/me")
def get_me_endpoint(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role.name if current_user.role else None,
    }

@router.get("/get_subroles", response_model=RolesResponse)
def get_subroles_endpoint(
    current_user: User = Depends(get_current_user)
) -> RolesResponse:
    user_role = current_user.role.name
    roles = get_subroles_for_role(user_role, excluded_roles=[user_role])
    return RolesResponse(roles=[RoleOut(name=name) for name in roles])

@router.post("/create")
def create_user_endpoint(
    data : UserWriter, 
    db : Session = Depends(get_db), 
    current_user : User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    return create_user_account(data, db, current_user)

@router.post("/edit_user/{user_id}")
def edit_user_endpoint(
    data : UserWriter, 
    db : Session = Depends(get_db),
    current_user : User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    return edit_user(data, db, current_user)

@router.get("/get/{user_id}")
def get_user_endpoint(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    return get_info_of_user(user_id, db, current_user)

@router.get("/get_user_stats")
def get_user_stats_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_count(db, current_user)

# TODO:
# Ensure usage of get_current_user and restructure service functions to work with that workflow