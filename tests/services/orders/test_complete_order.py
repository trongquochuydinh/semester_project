from fastapi import HTTPException
import pytest

from api.services.order_service import create_order, complete_order
from api.models import Order

def test_complete_restock_order_increases_stock(db, employee, item):
    initial_qty = item.quantity

    data = type("obj", (), {
        "order_type": "restock",
        "items": [{"item_id": item.id, "quantity": 3}],
    })()

    create_order(db, data, employee)

    order = db.query(Order).order_by(Order.id.desc()).first()

    response = complete_order(db, order.id, employee)

    db.flush()
    db.refresh(item)
    db.refresh(order)

    assert response.message.startswith("Order was successfully completed")
    assert order.status == "completed"
    assert item.quantity == initial_qty + 3

def test_cancel_order_twice(db, order, employee):
    complete_order(db, order.id, employee)

    with pytest.raises(HTTPException) as exc:
        complete_order(db, order.id, employee)

    assert exc.value.status_code == 409
