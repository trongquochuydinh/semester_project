from fastapi import HTTPException
import pytest


from api.services.order_service import cancel_order, create_order
from api.models import Order

def test_cancel_sale_order_restores_stock(db, employee, item):
    initial_qty = item.quantity

    data = type("obj", (), {
        "order_type": "sale",
        "items": [{"item_id": item.id, "quantity": 2}],
    })()

    create_order(db, data, employee)

    order = db.query(Order).order_by(Order.id.desc()).first()

    # stock was reduced at creation
    db.refresh(item)
    assert item.quantity == initial_qty - 2

    response = cancel_order(db, order.id, employee)

    db.flush()
    db.refresh(item)
    db.refresh(order)

    assert response.message.startswith("Order was successfully cancelled")
    assert order.status == "cancelled"
    assert item.quantity == initial_qty

def test_cancel_order_twice(db, order, employee):
    cancel_order(db, order.id, employee)

    with pytest.raises(HTTPException) as exc:
        cancel_order(db, order.id, employee)

    assert exc.value.status_code == 409

def test_cancel_order_not_found(db, order, employee):

    with pytest.raises(HTTPException) as exc:
        cancel_order(db, 999, employee)

    assert exc.value.status_code == 404
