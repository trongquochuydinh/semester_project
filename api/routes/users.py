from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, require_role, get_db
from api.models.user import User
from api.schemas import (
    LoginRequest, LoginResponse, 
    UserCreateResponse, UserCreateRequest, UserEditResponse, UserEditRequest, UserCountResponse, UserGetResponse,
    RolesResponse, RoleOut, MessageResponse, 
    PaginationRequest, PaginationResponse
)
from api.services import (
    login_user, 
    get_subroles_for_role, 
    create_user_account, 
    logout_user,  
    get_user_count, 
    get_info_of_user,
    edit_user,
    toggle_user_is_active,
    paginate_users
)

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/login", response_model=LoginResponse)
def login_user_endpoint(
    request: LoginRequest, 
    db: Session = Depends(get_db)
):
    return login_user(request.identifier, request.password, db)

@router.post("/logout", response_model=MessageResponse)
def logout_user_endpoint( 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    roles = get_subroles_for_role(
        db=db,
        role_name=current_user.role.name,
        excluded_roles=[current_user.role.name],
    )

    return RolesResponse(
        roles=[RoleOut(name=role.name) for role in roles]
    )

@router.post("/create", response_model=UserCreateResponse)
def create_user_endpoint(
    request : UserCreateRequest, 
    db : Session = Depends(get_db), 
    current_user : User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    return create_user_account(request, db, current_user)

@router.post("/edit_user/{user_id}", response_model=UserEditResponse)
def edit_user_endpoint(
    user_id: int,
    request : UserEditRequest, 
    db : Session = Depends(get_db),
    current_user : User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    return edit_user(user_id, request, db, current_user)

@router.get("/get/{user_id}", response_model=UserGetResponse)
def get_user_endpoint(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    return get_info_of_user(user_id, db, current_user)

@router.post("/toggle_user_is_active/{user_id}", response_model=MessageResponse)
def toggle_user_is_active_endpoint(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["superadmin", "admin", "manager"]))
):
    return toggle_user_is_active(user_id, db, current_user)

@router.get("/get_user_stats", response_model=UserCountResponse)
def get_user_stats_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_count(db, current_user)

@router.post("/paginate", response_model=PaginationResponse)
def paginate_users_endpoint(
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return paginate_users(
        db=db,
        limit=request.limit,
        offset=request.offset,
        filters=request.filters,
        user_role=current_user.role.name,
        company_id=current_user.company_id,
    )