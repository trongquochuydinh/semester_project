from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, require_role
from api.db.db_engine import get_db
from api.models.user import User
from api.schemas import (
    LoginRequest, LoginResponse, UserCreationResponse, UserEditRequest, UserWriter, RolesResponse, RoleOut, MessageResponse, PaginationRequest
)
from api.services import (
    login_user, 
    get_subroles_for_role, 
    create_user_account, 
    logout_user,  
    get_user_count, 
    get_info_of_user,
    edit_user,
    paginate_users
)

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/login", response_model=LoginResponse)
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

# Is this needed?
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
):
    roles = get_subroles_for_role(current_user.role.name, excluded_roles=[current_user.role.name])
    return RolesResponse(roles=[RoleOut(name=name) for name in roles])

@router.post("/create", response_model=UserCreationResponse)
def create_user_endpoint(
    data : UserWriter, 
    db : Session = Depends(get_db), 
    current_user : User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    return create_user_account(data, db, current_user)

@router.post("/edit_user/{user_id}", response_model=UserEditRequest)
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
    current_user: User = Depends(require_role(["superadmin", "admin"]))
):
    return get_user_count(db, current_user)

@router.post("/paginate")
def paginate_users_endpoint(
    data: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return paginate_users(
        db=db,
        limit=data.limit,
        offset=data.offset,
        filters=data.filters,
        user_role=current_user.role.name,
        company_id=current_user.company_id,
    )