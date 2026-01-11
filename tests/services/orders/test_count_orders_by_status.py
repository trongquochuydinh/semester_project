from api.services.order_service import count_orders_by_status

def test_count_orders_by_status_returns_all_keys(db, employee, order):
    result = count_orders_by_status(db, employee)

    assert set(result.keys()) == {"pending", "completed", "cancelled"}

def test_count_orders_by_status_counts_pending(db, employee, order):
    result = count_orders_by_status(db, employee)

    assert result["pending"] >= 1
