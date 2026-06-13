def test_admin_can_toggle_user_is_active(auth_client_factory, admin, employee):
    client = auth_client_factory(admin)

    response = client.patch(f"/api/users/{employee.id}/status")

    assert response.status_code == 200
    assert "successfully" in response.json()["message"].lower()


def test_employee_cant_toggle_admin_is_active(auth_client_factory, admin, employee):
    client = auth_client_factory(employee)

    response = client.patch(f"/api/users/{admin.id}/status")

    assert response.status_code == 403
