from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.domain.mappers.item_mapper import (
    item_domain_to_edit_response,
    item_domain_to_get_response,
    item_domain_to_row,
)
from api.models.user import User
from api.schemas import (
    ItemCreationRequest,
    ItemEditRequest,
    ItemEditResponse,
    ItemGetResponse,
    MessageResponse,
    PaginationRequest,
    PaginationResponse,
)
from api.services import (
    create_item,
    edit_item,
    get_item,
    paginate_items,
    toggle_item_is_active,
)

router = APIRouter(prefix="/api/items", tags=["items"])


@router.post("/search", response_model=PaginationResponse)
def paginate_items_endpoint(
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = paginate_items(
        db=db,
        current_user=current_user,
        limit=request.limit,
        offset=request.offset,
        filters=request.filters,
    )
    return PaginationResponse(
        total=result.total,
        data=[item_domain_to_row(item) for item in result.data],
    )


@router.get("/{item_id}", response_model=ItemGetResponse)
def get_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_item(item_id=item_id, db=db, current_user=current_user)


@router.post("", response_model=MessageResponse)
def create_item_endpoint(
    request: ItemCreationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = create_item(
        db=db,
        current_user=current_user,
        name=request.name,
        price=request.price,
        quantity=request.quantity,
    )
    return MessageResponse(message=result.message)


@router.put("/{item_id}", response_model=ItemEditResponse)
def edit_item_endpoint(
    item_id: int,
    request: ItemEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return edit_item(
        item_id=item_id,
        db=db,
        current_user=current_user,
        name=request.name,
        price=request.price,
        quantity=request.quantity,
    )


@router.patch("/{item_id}/status", response_model=MessageResponse)
def toggle_item_is_active_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = toggle_item_is_active(item_id=item_id, db=db, current_user=current_user)
    return MessageResponse(message=result.message)
