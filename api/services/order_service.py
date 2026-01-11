from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.models import User, Item, Order, OrderItem
from api.schemas import (
    PaginationResponse,
    MessageResponse,
    OrderCreateRequest
)

from api.db.order_db import (
    paginate_order as db_paginate_orders,
    insert_order as db_insert_order,
    get_order_by_id as db_get_order_by_id,
    change_order_status as db_change_order_status,
    count_orders_grouped_by_status as db_count_orders_grouped_by_status
)

from api.db.order_items_db import (
    paginate_order_items as db_paginate_order_items,
    insert_order_item as db_insert_order_item,
    get_order_items as db_get_order_items
)

from api.db.item_db import (
    get_item_data_by_id as db_get_item_data_by_id,
    apply_stock_change as db_apply_stock_change
)

from api.services.company_service import assert_company_access
from api.utils import validate_order_type, validate_order_item, start_of_day, end_of_day

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

def create_order(db: Session, data: OrderCreateRequest, current_user: User):
    order_type: str = validate_order_type(data.order_type)
    validated_items: List = []

    for order_item in data.items:
        item: Item = db_get_item_data_by_id(db, order_item["item_id"])
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        assert_company_access(
            db=db,
            is_superadmin=False,
            current_user_company_id=current_user.company_id,
            company_id=item.company_id,
        )

        validated = validate_order_item(
            item=item,
            quantity=order_item["quantity"],
            order_type=order_type,
        )

        validated_items.append(validated)

    order = Order(
        status="pending",
        order_type=order_type,
        user_id=current_user.id,
        company_id=current_user.company_id
    )

    db_insert_order(db, order)

    for v in validated_items:
        order_item = OrderItem(
            order_id=order.id,
            item_id=v["item"].id,
            quantity=v["quantity"],
            unit_price=v["unit_price"],
        )

        db_insert_order_item(db, order_item)

        if order_type == "sale":
            db_apply_stock_change(db, v["item"], -v["quantity"])

    return MessageResponse(
        message="Order was successfully created."
    )

def cancel_order(db: Session, order_id: int, current_user: User):
    order = db_get_order_by_id(db, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    assert_company_access(
        db=db,
        is_superadmin=False,
        current_user_company_id=current_user.company_id,
        company_id=order.company_id
    )

    if order.status == "cancelled":
        raise HTTPException(
            status_code=409,
            detail="Order is already cancelled"
        )

    if order.status == "completed":
        raise HTTPException(
            status_code=409,
            detail="Completed orders cannot be cancelled"
        )

    order_items = db_get_order_items(db, order.id)

    for oi in order_items:
        item = oi.item  # ORM relationship

        if order.order_type == "sale":
            db_apply_stock_change(db, item, oi.quantity)
        elif order.order_type == "restock":
            db_apply_stock_change(db, item, -oi.quantity)

    db_change_order_status(order, "cancelled")

    return MessageResponse(
        message=f"Order was successfully cancelled."
    )

def complete_order(db: Session, order_id: int, current_user: User):
    order = db_get_order_by_id(db, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    assert_company_access(
        db=db,
        is_superadmin=False,
        current_user_company_id=current_user.company_id,
        company_id=order.company_id
    )

    if order.status == "cancelled":
        raise HTTPException(
            status_code=409,
            detail="Order is already cancelled"
        )

    if order.status == "completed":
        raise HTTPException(
            status_code=409,
            detail="Completed orders cannot be cancelled"
        )

    order_items = db_get_order_items(db, order.id)

    for oi in order_items:
        item = oi.item

        if order.order_type == "restock":
            db_apply_stock_change(db, item, oi.quantity)

    db_change_order_status(order, "completed")

    return MessageResponse(
        message=f"Order was successfully completed."
    )

def count_orders_by_status(
    db: Session,
    current_user: User,
):
    now = datetime.utcnow()

    filters = {
        "order_type": "sale",
        "from_ts": start_of_day(now - timedelta(days=7)),
        "to_ts": end_of_day(now),
    }

    rows = db_count_orders_grouped_by_status(
        db=db,
        company_id=current_user.company_id,
        is_superadmin=(current_user.role.name == "superadmin"),
        filters=filters,
    )

    result = {status: 0 for status in ("pending", "completed", "cancelled")}

    for status, count in rows:
        result[status] = count

    return result
