def test_get_company_success(auth_client_factory, superadmin, company):
    client = auth_client_factory(superadmin)

    response = client.get(f"/api/companies/{company.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == company.id
    assert body["name"] == company.name
    assert body["field"] == company.field


def test_get_company_not_found(auth_client_factory, superadmin):
    client = auth_client_factory(superadmin)

    response = client.get("/api/companies/9999")

    assert response.status_code == 404
