import pytest
from decimal import Decimal

from api.domain import ConflictError, ForbiddenError, ValidationError
from api.domain.order import (
    Order,
    OrderLineItem,
    OrderStatus,
    OrderType,
    StockAdjustment,
)


def _line(qty=2):
    return OrderLineItem(
        item_id=1,
        name="Widget",
        quantity=qty,
        unit_price=Decimal("10.00"),
    )


def test_order_type_from_raw():
    assert OrderType.from_raw("sale") == OrderType.SALE


def test_order_type_rejects_invalid():
    with pytest.raises(ValidationError):
        OrderType.from_raw("invalid")


def test_order_cancel_sale_restores_stock():
    order = Order.draft("sale", user_id=1, company_id=1)
    order.add_line(_line(3))

    adjustments = order.cancel()

    assert order.status == OrderStatus.CANCELLED
    assert adjustments == [StockAdjustment(item_id=1, delta=3)]


def test_order_cancel_restock_reverses_stock():
    order = Order.draft("restock", user_id=1, company_id=1)
    order.add_line(_line(2))

    adjustments = order.cancel()

    assert adjustments == [StockAdjustment(item_id=1, delta=-2)]


def test_order_cancel_rejects_completed():
    order = Order.draft("sale", user_id=1, company_id=1)
    order.status = OrderStatus.COMPLETED

    with pytest.raises(ConflictError):
        order.cancel()


def test_order_complete_restock_adds_stock():
    order = Order.draft("restock", user_id=1, company_id=1)
    order.add_line(_line(4))

    adjustments = order.complete()

    assert order.status == OrderStatus.COMPLETED
    assert adjustments == [StockAdjustment(item_id=1, delta=4)]


def test_order_line_rejects_insufficient_stock():
    with pytest.raises(ForbiddenError):
        OrderLineItem.from_request(
            item_id=1,
            name="Widget",
            quantity=10,
            unit_price=Decimal("1"),
            is_active=True,
            available_quantity=2,
            order_type=OrderType.SALE,
        )


def test_order_create_sale_adjustments():
    order = Order.draft("sale", user_id=1, company_id=1)
    order.add_line(_line(2))

    assert order.create_stock_adjustments() == [StockAdjustment(item_id=1, delta=-2)]
