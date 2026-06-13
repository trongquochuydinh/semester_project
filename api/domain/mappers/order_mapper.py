from typing import List, Optional

from api.domain.order import (
    Order as DomainOrder,
    OrderLineItem,
    OrderStatus,
    OrderType,
)
from api.models.order import Order as OrderEntity
from api.models.order_item import OrderItem


def order_entity_to_domain(
    order: OrderEntity,
    lines: Optional[List[OrderItem]] = None,
) -> DomainOrder:
    domain = DomainOrder(
        id=order.id,
        status=OrderStatus(order.status),
        order_type=OrderType(order.order_type),
        user_id=order.user_id,
        company_id=order.company_id,
        created_at_fmt=getattr(order, "created_at_fmt", None),
        completed_at_fmt=getattr(order, "completed_at_fmt", None),
    )
    if lines:
        for order_item in lines:
            domain.add_line(
                OrderLineItem(
                    item_id=order_item.item_id,
                    name=order_item.item.name if order_item.item else "",
                    quantity=order_item.quantity,
                    unit_price=order_item.unit_price,
                )
            )
    return domain


def order_domain_to_row(order: DomainOrder) -> dict:
    return {
        "id": order.id,
        "status": order.status.value,
        "order_type": order.order_type.value,
        "user_id": order.user_id,
        "company_id": order.company_id,
        "created_at_fmt": order.created_at_fmt,
        "completed_at_fmt": order.completed_at_fmt,
    }


def order_line_to_row(line: OrderLineItem) -> dict:
    return {
        "name": line.name,
        "price": line.unit_price,
        "quantity": line.quantity,
    }


def order_lines_to_rows(lines: List[OrderLineItem]) -> List[dict]:
    return [order_line_to_row(line) for line in lines]
