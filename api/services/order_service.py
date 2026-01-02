from sqlalchemy.orm import Session

from api.models.user import User
from api.schemas import (
    PaginationResponse
)

from api.db.order_db import (
    paginate_order as db_paginate_orders,
)

from api.db.order_items_db import (
    paginate_order_items as db_paginate_order_items
)

def paginate_orders(
    db: Session,
    limit: int,
    offset: int,
    filters: dict,
    company_id: int,
):
    
    total, results = db_paginate_orders(
        db=db,
        filters=filters,
        company_id=company_id,
        limit=limit,
        offset=offset,
    )

    def serialize(i):
        d = {c.name: getattr(i, c.name) for c in i.__table__.columns}
        d["created_at_fmt"] = getattr(i, "created_at_fmt", None)
        d["completed_at_fmt"] = getattr(i, "completed_at_fmt", None)
        return d

    return PaginationResponse(
        total=total,
        data=[serialize(r) for r in results],
    )

def paginate_order_items(
    db: Session,
    order_id: int,
    company_id: int,
    limit: int,
    offset: int,
):
    total, results = db_paginate_order_items(
        db=db,
        order_id=order_id,
        company_id=company_id,
        limit=limit,
        offset=offset,
    )

    data = []
    for item, ordered_quantity, unit_price in results:
        d = {
            "name": item.name,
            "price": unit_price,
            "quantity": ordered_quantity,
        }
        data.append(d)

    return PaginationResponse(
        total=total,
        data=data,
    )

def create_order(data, db: Session, current_user: User):
    # check that the type of order is correct
    # need to check the validity of the items
    # user role was checked in the dependancy of create order route
    # to which this order belongs to will be determined by the current user
    # need to link inserts into both order and order-items tables

    # TODO: make sure that the items inside the create order modal are only those that are ACTIVE
    return

def cancel_order(order_id: int):
    return

def complete_order(order_id: int):
    return