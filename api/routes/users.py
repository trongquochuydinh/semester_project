from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from api.db.user_db import get_oauth_providers, get_user_data_by_id
from api.dependencies import get_current_user, require_role, get_db
from api.models.user import User
from api.schemas import (
    LoginRequest, LoginResponse, 
    UserCreateResponse, UserCreateRequest, UserEditResponse, UserEditRequest, UserCountResponse, UserGetResponse,
    RolesResponse, RoleOut, MessageResponse, 
    PaginationRequest, PaginationResponse
)
from api.schemas.user_schema import OAuthInfo
from api.services import (
    login_user, 
    get_subroles_for_role, 
    create_user_account, 
    logout_user,  
    get_user_count, 
    get_info_of_user,
    edit_user,
    toggle_user_is_active,
    paginate_users,
    get_current_user_info
)
from api.services.auth_service import handle_github_callback, start_github_link, start_github_login

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/login", response_model=LoginResponse)
def login_user_endpoint(
    request: LoginRequest, 
    db: Session = Depends(get_db)
):
    return login_user(request.identifier, request.password, db)

@router.get("/auth/github/login")
def github_login():
    redirect_url = start_github_login()
    return {"redirect_url": redirect_url}

@router.get("/auth/github/link")
def link_github_account(
    current_user = Depends(get_current_user),
):
    redirect_url = start_github_link(current_user.id)
    return {"redirect_url": redirect_url}

@router.get("/auth/github/callback")
def github_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):
    redirect_url = handle_github_callback(code, state, db)
    return RedirectResponse(url=redirect_url)

@router.post("/logout", response_model=MessageResponse)
def logout_user_endpoint( 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return logout_user(current_user, db)

# For future profile edit
@router.get("/me")
def get_me_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_current_user_info(db, current_user)

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

@router.post("/edit/{user_id}", response_model=UserEditResponse)
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