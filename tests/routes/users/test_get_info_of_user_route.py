def test_admin_can_get_user(auth_client_factory, admin, employee):
    client = auth_client_factory(admin)

    response = client.get(f"/api/users/get/{employee.id}")

    assert response.status_code == 200
    body = response.json()

    assert body["username"] == employee.username
    assert body["email"] == employee.email

def test_employee_cant_get_admin(auth_client_factory, admin, employee):
    client = auth_client_factory(employee)

    response = client.get(f"/api/users/get/{admin.id}")

    assert response.status_code == 403

