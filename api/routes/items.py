from fastapi import APIRouter, Body, Depends

from sqlalchemy.orm import Session
from api.dependencies import get_current_user, require_role, get_db
from api.models.user import User
from api.schemas import(
    PaginationRequest,
    ItemCreationRequest,
    ItemEditRequest,
    ItemEditResponse
)

from api.services import (
    create_item,
    edit_item,
    get_item,
    paginate_items,
    toggle_item_is_active
)

router = APIRouter(prefix="/api/items", tags=["items"])

@router.post("/paginate")
def paginate_items_endpoint(
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return paginate_items(
        db=db,
        limit=request.limit,
        offset=request.offset,
        filters=request.filters,
        company_id=current_user.company_id,
    )

@router.post("/create")
def create_item_endpoint(
    request: ItemCreationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    return create_item(request, db, current_user)

@router.post("/edit/{item_id}", response_model=ItemEditResponse)
def edit_item_endpoint(
    item_id: int,
    request: ItemEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    return edit_item(item_id, request, db, current_user)

@router.post("/toggle_item_is_active/{item_id}")
def toggle_item_is_active_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin", "manager"]))
):
    return toggle_item_is_active(item_id, db, current_user)

@router.get("/get/{item_id}")
def get_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    return get_item(item_id, db, current_user)