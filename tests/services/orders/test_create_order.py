from fastapi import HTTPException
import pytest


from api.services.order_service import create_order
from api.schemas import OrderCreateRequest

def test_create_sale_order_success(db, employee, item):
    initial_qty = item.quantity

    data = type("obj", (), {
        "order_type": "sale",
        "items": [{"item_id": item.id, "quantity": 2}],
    })()

    response = create_order(db, data, employee)

    db.flush()
    db.refresh(item)

    assert response.message == "Order was successfully created."
    assert item.quantity == initial_qty - 2

def test_create_order_item_not_found(db, employee):
    data = type("obj", (), {
        "order_type": "sale",
        "items": [{"item_id": 9999, "quantity": 1}],
    })()

    with pytest.raises(HTTPException) as exc:
        create_order(db, data, employee)

    assert exc.value.status_code == 404

def test_create_order_cross_company_item_forbidden(
    db, employee, item, company2
):
    item.company_id = company2.id
    db.flush()

    data = type("obj", (), {
        "order_type": "sale",
        "items": [{"item_id": item.id, "quantity": 1}],
    })()

    with pytest.raises(HTTPException) as exc:
        create_order(db, data, employee)

    assert exc.value.status_code == 403

def test_create_order_empty_fields(db, employee):
    data = OrderCreateRequest(
        order_type="",
        items=[]
    )

    with pytest.raises(HTTPException) as exc:
        create_order(db, data, employee)

    assert exc.value.status_code == 422