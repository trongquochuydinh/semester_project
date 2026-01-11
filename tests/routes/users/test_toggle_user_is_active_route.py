def test_admin_can_toggle_user_is_active(auth_client_factory, admin, employee):
    client = auth_client_factory(admin)

    response = client.post(
        f"/api/users/toggle_user_is_active/{employee.id}"
    )

    assert response.status_code == 200
    assert "successfully" in response.json()["message"].lower()

def test_employee_cant_toggle_admin_is_active(auth_client_factory, admin, employee):
    client = auth_client_factory(employee)

    response = client.post(
        f"/api/users/toggle_user_is_active/{admin.id}"
    )

    assert response.status_code == 403
