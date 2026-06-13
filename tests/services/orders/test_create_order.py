import pytest

from api.domain import ForbiddenError, NotFoundError, ValidationError
from api.services.order_service import create_order


def test_create_sale_order_success(db, employee, item):
    initial_qty = item.quantity

    response = create_order(
        db=db,
        current_user=employee,
        order_type="sale",
        items=[{"item_id": item.id, "quantity": 2}],
    )

    db.flush()
    db.refresh(item)

    assert response.message == "Order was successfully created."
    assert item.quantity == initial_qty - 2


def test_create_order_item_not_found(db, employee):
    with pytest.raises(NotFoundError):
        create_order(
            db=db,
            current_user=employee,
            order_type="sale",
            items=[{"item_id": 9999, "quantity": 1}],
        )


def test_create_order_cross_company_item_forbidden(db, employee, item, company2):
    item.company_id = company2.id
    db.flush()

    with pytest.raises(ForbiddenError):
        create_order(
            db=db,
            current_user=employee,
            order_type="sale",
            items=[{"item_id": item.id, "quantity": 1}],
        )


def test_create_order_empty_fields(db, employee):
    with pytest.raises(ValidationError):
        create_order(
            db=db,
            current_user=employee,
            order_type="",
            items=[],
        )
