def test_admin_can_get_user_stats(auth_client_factory, admin):
    client = auth_client_factory(admin)

    response = client.get("/api/users/get_user_stats")

    assert response.status_code == 200
    body = response.json()

    assert "total_users" in body
    assert "online_users" in body
