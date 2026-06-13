from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session

from api.domain import MessageResult, NotFoundError, ValidationError
from api.domain.access import RolePolicy
from api.domain.mappers.item_mapper import item_entity_to_domain
from api.domain.mappers.order_mapper import (
    order_domain_to_row,
    order_entity_to_domain,
    order_line_to_row,
    order_lines_to_rows,
)
from api.domain.order import (
    Order as DomainOrder,
    OrderLineItem,
    OrderStatusCounts,
    OrderType,
    PaginatedOrderItems,
    PaginatedOrders,
)
from api.models import Order, OrderItem, User
from api.db.order_db import (
    paginate_order as db_paginate_orders,
    insert_order as db_insert_order,
    get_order_by_id as db_get_order_by_id,
    change_order_status as db_change_order_status,
    count_orders_grouped_by_status as db_count_orders_grouped_by_status,
)
from api.db.order_items_db import (
    paginate_order_items as db_paginate_order_items,
    insert_order_item as db_insert_order_item,
    get_order_items as db_get_order_items,
)
from api.db.item_db import (
    get_item_data_by_id as db_get_item_data_by_id,
    apply_stock_change as db_apply_stock_change,
)
from api.services.company_service import assert_company_access
from api.utils import start_of_day, end_of_day


def _is_superadmin(user: User) -> bool:
    return user.role.name == "superadmin"


def _apply_adjustments(db: Session, adjustments) -> None:
    for adjustment in adjustments:
        item = db_get_item_data_by_id(db, adjustment.item_id)
        if item:
            db_apply_stock_change(db, item, adjustment.delta)


def create_order(
    db: Session,
    current_user: User,
    order_type: str,
    items: List[dict],
) -> MessageResult:
    RolePolicy.require(current_user.role.name, ["admin", "manager", "employee"])

    if not items:
        raise ValidationError("Order must contain at least one item")

    order = DomainOrder.draft(
        order_type=order_type,
        user_id=current_user.id,
        company_id=current_user.company_id,
    )

    for order_item in items:
        entity = db_get_item_data_by_id(db, order_item["item_id"])
        if not entity:
            raise NotFoundError("Item not found")

        assert_company_access(
            db=db,
            is_superadmin=_is_superadmin(current_user),
            current_user_company_id=current_user.company_id,
            company_id=entity.company_id,
        )

        domain_item = item_entity_to_domain(entity)
        domain_item.can_fulfill(order_item["quantity"], order.order_type.value)

        order.add_line(
            OrderLineItem.from_request(
                item_id=entity.id,
                name=entity.name,
                quantity=order_item["quantity"],
                unit_price=entity.price,
                is_active=entity.is_active,
                available_quantity=entity.quantity,
                order_type=order.order_type,
            )
        )

    order_entity = Order(
        status=order.status.value,
        order_type=order.order_type.value,
        user_id=order.user_id,
        company_id=order.company_id,
    )
    db_insert_order(db, order_entity)

    for line in order.lines:
        db_insert_order_item(
            db,
            OrderItem(
                order_id=order_entity.id,
                item_id=line.item_id,
                quantity=line.quantity,
                unit_price=line.unit_price,
            ),
        )

    _apply_adjustments(db, order.create_stock_adjustments())

    return MessageResult(message="Order was successfully created.")


def cancel_order(db: Session, order_id: int, current_user: User) -> MessageResult:
    RolePolicy.require(current_user.role.name, ["admin", "manager", "employee"])

    order_entity = db_get_order_by_id(db, order_id)
    if not order_entity:
        raise NotFoundError("Order not found")

    assert_company_access(
        db=db,
        is_superadmin=_is_superadmin(current_user),
        current_user_company_id=current_user.company_id,
        company_id=order_entity.company_id,
    )

    order_items = db_get_order_items(db, order_entity.id)
    order = order_entity_to_domain(order_entity, order_items)
    adjustments = order.cancel()

    _apply_adjustments(db, adjustments)
    db_change_order_status(order_entity, order.status.value)

    return MessageResult(message="Order was successfully cancelled.")


def complete_order(db: Session, order_id: int, current_user: User) -> MessageResult:
    RolePolicy.require(current_user.role.name, ["admin", "manager", "employee"])

    order_entity = db_get_order_by_id(db, order_id)
    if not order_entity:
        raise NotFoundError("Order not found")

    assert_company_access(
        db=db,
        is_superadmin=_is_superadmin(current_user),
        current_user_company_id=current_user.company_id,
        company_id=order_entity.company_id,
    )

    order_items = db_get_order_items(db, order_entity.id)
    order = order_entity_to_domain(order_entity, order_items)
    adjustments = order.complete()

    _apply_adjustments(db, adjustments)
    db_change_order_status(order_entity, order.status.value)

    return MessageResult(message="Order was successfully completed.")


def paginate_orders(
    db: Session,
    current_user: User,
    limit: int,
    offset: int,
    filters: dict,
) -> PaginatedOrders:
    RolePolicy.require(current_user.role.name, ["admin", "manager"])

    total, results = db_paginate_orders(
        db=db,
        filters=filters,
        company_id=current_user.company_id,
        limit=limit,
        offset=offset,
    )

    return PaginatedOrders(
        total=total,
        data=[order_entity_to_domain(order) for order in results],
    )


def paginate_order_items(
    db: Session,
    current_user: User,
    order_id: int,
    limit: int,
    offset: int,
) -> PaginatedOrderItems:
    RolePolicy.require(current_user.role.name, ["admin", "manager"])

    total, results = db_paginate_order_items(
        db=db,
        order_id=order_id,
        company_id=current_user.company_id,
        limit=limit,
        offset=offset,
    )

    lines = []
    for item, ordered_quantity, unit_price in results:
        lines.append(
            OrderLineItem(
                item_id=item.id,
                name=item.name,
                quantity=ordered_quantity,
                unit_price=unit_price,
            )
        )

    return PaginatedOrderItems(total=total, data=lines)


def count_orders_by_status(db: Session, current_user: User) -> OrderStatusCounts:
    now = datetime.utcnow()
    filters = {
        "order_type": "sale",
        "from_ts": start_of_day(now - timedelta(days=7)),
        "to_ts": end_of_day(now),
    }

    rows = db_count_orders_grouped_by_status(
        db=db,
        company_id=current_user.company_id,
        is_superadmin=_is_superadmin(current_user),
        filters=filters,
    )

    counts = {"pending": 0, "completed": 0, "cancelled": 0}
    for status, count in rows:
        counts[status] = count

    return OrderStatusCounts(
        pending=counts["pending"],
        completed=counts["completed"],
        cancelled=counts["cancelled"],
    )
