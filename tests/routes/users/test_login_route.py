from api.services.user_service import get_info_of_user

def test_login_success(client_with_db, admin, db):
    response = client_with_db.post(
        "/api/users/login",
        json={
            "identifier": admin.email,
            "password": "admin123",
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert "access_token" in body
    assert body["username"] == admin.username
    assert body["role"] == admin.role.name

    db.flush()
    db.refresh(admin)

    assert admin.is_active is True
    assert admin.session_id is not None
    assert admin.status == "online"


def test_login_incorrect_credentials(client_with_db):
    response = client_with_db.post(
        "/api/users/login",
        json={
            "identifier": "nonexistant",
            "password": "admin123",
        },
    )

    assert response.status_code == 406
    body = response.json()
    assert body["detail"] == "Invalid username or password"

def test_login_fail1(client_with_db, admin, employee):
    response = client_with_db.post(
        "/api/users/login",
        json={
            "identifier": employee.email,
            "password": "admin123",
        },
    )

    assert response.status_code == 406
    body = response.json()
    assert body["detail"] == "Invalid username or password"

def test_unauthenticated_user_cannot_create_user(client_with_db, company):
    response = client_with_db.post(
        "/api/users/create",
        json={
            "username": "x",
            "email": "x@example.com",
            "role": "employee",
            "company_id": company.id,
        },
    )

    assert response.status_code in (401, 403)
    assert response.json()["detail"] == "Not authenticated"

def test_logout_success(auth_client_factory, admin, db):
    client = auth_client_factory(admin)

    response = client.post("/api/users/logout")

    assert response.status_code == 200
    body = response.json()
    assert "successfully" in body["message"].lower()

def test_unauthenticated_user_cannot_logout(client_with_db):
    response = client_with_db.post("/api/users/logout")

    assert response.status_code in (401, 403)
    assert response.json()["detail"] == "Not authenticated"
