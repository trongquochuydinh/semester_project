def test_admin_can_create_item(auth_client_factory, admin):
    client = auth_client_factory(admin)

    response = client.post(
        "/api/items",
        json={"name": "Route Item", "price": "19.99", "quantity": 3},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Item was successfully added."
