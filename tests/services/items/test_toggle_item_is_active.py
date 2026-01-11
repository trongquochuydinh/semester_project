import pytest

from api.services.item_service import toggle_item_is_active

def test_toggle_item_is_active(db, admin, item):
    assert item.is_active is True

    response = toggle_item_is_active(
        item_id=item.id,
        db=db,
        current_user=admin,
    )

    db.flush()
    db.refresh(item)

    assert item.is_active is False
    assert "discontinued" in response.message.lower()


def test_toggle_item_is_active_twice(db, admin, item):
    assert item.is_active is True
    toggle_item_is_active(item.id, db, admin)
    assert item.is_active is False
    toggle_item_is_active(item.id, db, admin)

    db.flush()
    db.refresh(item)
    assert item.is_active is True
