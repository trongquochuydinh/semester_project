from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.models.user import User
from api.schemas import (
    MessageResponse,
    PaginationRequest,
    PaginationResponse,
    RoleOut,
    RolesResponse,
    UserCountResponse,
    UserCreateRequest,
    UserCreateResponse,
    UserEditRequest,
    UserEditResponse,
    UserGetResponse,
)
from api.services import (
    create_user_account,
    edit_user,
    get_current_user_info,
    get_info_of_user,
    get_subroles_for_role,
    get_user_count,
    paginate_users,
    toggle_user_is_active,
)

# Create router for user-related endpoints
router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me")
def get_me_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_current_user_info(db, current_user)


@router.get("/roles/assignable", response_model=RolesResponse)
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


@router.get("/stats", response_model=UserCountResponse)
def get_user_stats_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_count(db, current_user)


@router.post("", response_model=UserCreateResponse)
def create_user_endpoint(
    request: UserCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_user_account(
        db=db,
        current_user=current_user,
        username=request.username,
        email=request.email,
        role=request.role,
        company_id=request.company_id,
    )


@router.put("/{user_id}", response_model=UserEditResponse)
def edit_user_endpoint(
    user_id: int,
    request: UserEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return edit_user(
        db=db,
        current_user=current_user,
        user_id=user_id,
        username=request.username,
        email=request.email,
        role=request.role,
        company_id=request.company_id,
    )


@router.get("/{user_id}", response_model=UserGetResponse)
def get_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_info_of_user(db=db, current_user=current_user, user_id=user_id)


@router.patch("/{user_id}/status", response_model=MessageResponse)
def toggle_user_is_active_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = toggle_user_is_active(db=db, current_user=current_user, user_id=user_id)
    return MessageResponse(message=result.message)


@router.post("/search", response_model=PaginationResponse)
def paginate_users_endpoint(
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = paginate_users(
        db=db,
        current_user=current_user,
        limit=request.limit,
        offset=request.offset,
        filters=request.filters,
    )
    return PaginationResponse(total=result.total, data=result.data)