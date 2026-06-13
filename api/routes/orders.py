from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.domain.mappers.order_mapper import (
    order_domain_to_row,
    order_lines_to_rows,
)
from api.models.user import User
from api.schemas import MessageResponse, OrderCreateRequest, PaginationRequest, PaginationResponse
from api.services import (
    cancel_order,
    complete_order,
    count_orders_by_status,
    create_order,
    paginate_order_items,
    paginate_orders,
)

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("/search", response_model=PaginationResponse)
def paginate_orders_endpoint(
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = paginate_orders(
        db=db,
        current_user=current_user,
        limit=request.limit,
        offset=request.offset,
        filters=request.filters,
    )
    return PaginationResponse(
        total=result.total,
        data=[order_domain_to_row(order) for order in result.data],
    )


@router.post("/{order_id}/items/search", response_model=PaginationResponse)
def paginate_order_items_endpoint(
    order_id: int,
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = paginate_order_items(
        db=db,
        current_user=current_user,
        order_id=order_id,
        limit=request.limit,
        offset=request.offset,
    )
    return PaginationResponse(
        total=result.total,
        data=order_lines_to_rows(result.data),
    )


@router.get("/stats")
def get_order_counts_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return count_orders_by_status(db=db, current_user=current_user).as_dict()


@router.post("", response_model=MessageResponse)
def create_order_endpoint(
    data: OrderCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = create_order(
        db=db,
        current_user=current_user,
        order_type=data.order_type,
        items=data.items,
    )
    return MessageResponse(message=result.message)


@router.post("/{order_id}/cancel", response_model=MessageResponse)
def cancel_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = cancel_order(db=db, order_id=order_id, current_user=current_user)
    return MessageResponse(message=result.message)


@router.post("/{order_id}/complete", response_model=MessageResponse)
def complete_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = complete_order(db=db, order_id=order_id, current_user=current_user)
    return MessageResponse(message=result.message)
