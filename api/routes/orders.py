from fastapi import APIRouter, Body, Depends

from sqlalchemy.orm import Session
from api.dependencies import get_current_user, require_role, get_db
from api.models.user import User
from api.schemas import(
    PaginationRequest,
    OrderCreateRequest,
    MessageResponse
)

from api.services import (
    paginate_orders,
    paginate_order_items,
    create_order,
    cancel_order,
    complete_order,
    count_orders_by_status
)

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/paginate")
def paginate_orders_endpoint(
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"])),
):
    return paginate_orders(
        db=db,
        limit=request.limit,
        offset=request.offset,
        filters=request.filters,
        company_id=current_user.company_id,
    )

@router.post("/{order_id}/items/paginate")
def paginate_order_items_endpoint(
    order_id: int,
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"])),
):
    return paginate_order_items(
        db=db,
        order_id=order_id,
        company_id=current_user.company_id,
        limit=request.limit,
        offset=request.offset,
    )

@router.post("/create", response_model=MessageResponse)
def create_order_endpoint(
    data: OrderCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"])),
):
    return create_order(
        db=db,
        data=data,
        current_user=current_user,
    )

@router.post("/cancel/{order_id}")
def cancel_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"])),
):
    return cancel_order(
        db=db,
        order_id=order_id,
        current_user=current_user,
    )

@router.post("/complete/{order_id}")
def complete_order_endpoint(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "manager"])),
):
    return complete_order(
        db=db,
        order_id=order_id,
        current_user=current_user,
    )

@router.get("/order_counts")
def get_order_counts_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return count_orders_by_status(
        db=db,
        current_user=current_user,
    )