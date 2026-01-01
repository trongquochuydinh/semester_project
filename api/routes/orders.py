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
    paginate_orders
)

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/paginate")
def paginate_orders_endpoint(
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return paginate_orders(
        db=db,
        limit=request.limit,
        offset=request.offset,
        filters=request.filters,
        company_id=current_user.company_id,
    )