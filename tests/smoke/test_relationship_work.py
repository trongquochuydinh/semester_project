def test_full_relationship_graph(
    company,
    admin,
    employee,
    item,
    order,
    order_item,
):
    # --- Company level ---
    assert company.id is not None

    # Company → Users
    assert admin.company_id == company.id
    assert employee.company_id == company.id
    assert admin in company.users
    assert employee in company.users

    # Company → Items
    assert item.company_id == company.id
    assert item in company.items

    # --- Order level ---
    assert order.company_id == company.id
    assert order.user_id == employee.id
    assert order.user == employee
    assert order.company == company

    # --- OrderItem level ---
    assert order_item.order_id == order.id
    assert order_item.item_id == item.id

    assert order_item in order.items
    assert order_item in item.order_items

    # --- Cross-checks ---
    assert order_item.order.company_id == company.id
    assert order_item.item.company_id == company.id
