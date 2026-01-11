def test_admin_can_create_user(auth_client_factory, admin, company, role_employee):
    client = auth_client_factory(admin)

    response = client.post(
        "/api/users/create",
        json={
            "username": "new_user",
            "email": "new_user@example.com",
            "role": "employee",
            "company_id": company.id,
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert body["message"] == "User created successfully"
    assert "initial_password" in body

def test_employee_cant_create_user(auth_client_factory, employee, company, role_employee):
    client = auth_client_factory(employee)

    response = client.post(
        "/api/users/create",
        json={
            "username": "new_user",
            "email": "new_user@example.com",
            "role": "employee",
            "company_id": company.id,
        },
    )

    assert response.status_code == 403