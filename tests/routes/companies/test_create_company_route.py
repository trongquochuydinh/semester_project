def test_superadmin_can_create_company(auth_client_factory, superadmin):
    client = auth_client_factory(superadmin)

    response = client.post(
        "/api/companies",
        json={"name": "RouteCo", "field": "IT"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Company created successfully."


def test_admin_cannot_create_company(auth_client_factory, admin):
    client = auth_client_factory(admin)

    response = client.post(
        "/api/companies",
        json={"name": "RouteCo2", "field": "IT"},
    )

    assert response.status_code == 403
