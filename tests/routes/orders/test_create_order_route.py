def test_employee_can_create_order(auth_client_factory, employee, item):
    client = auth_client_factory(employee)

    response = client.post(
        "/api/orders",
        json={
            "order_type": "sale",
            "items": [{"item_id": item.id, "quantity": 1}],
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Order was successfully created."
