def test_superadmin_can_list_companies(auth_client_factory, superadmin, company, company2):
    client = auth_client_factory(superadmin)

    response = client.get("/api/companies")

    assert response.status_code == 200
    body = response.json()
    ids = {c["id"] for c in body["companies"]}
    assert company.id in ids
    assert company2.id in ids


def test_admin_can_list_companies(auth_client_factory, admin, company):
    client = auth_client_factory(admin)

    response = client.get("/api/companies")

    assert response.status_code == 200
    body = response.json()
    ids = {c["id"] for c in body["companies"]}
    assert ids == {company.id}
