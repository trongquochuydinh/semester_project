def test_admin_can_edit_user(auth_client_factory, admin, employee, company):
    client = auth_client_factory(admin)

    response = client.post(
        f"/api/users/edit/{employee.id}",
        json={
            "username": "new_user",
            "email": "new_user@example.com",
            "role": "employee",
            "company_id": company.id,
        },
    )

    assert response.status_code == 200

def test_employee_can_edit_manager(auth_client_factory, manager, employee, company):
    client = auth_client_factory(employee)

    response = client.post(
        f"/api/users/edit/{manager.id}",
        json={
            "username": "new_user",
            "email": "new_user@example.com",
            "role": "admin",
            "company_id": company.id,
        },
    )

    assert response.status_code == 403