def test_superadmin_can_search_companies(auth_client_factory, superadmin, company):
    client = auth_client_factory(superadmin)

    response = client.post(
        "/api/companies/search",
        json={"limit": 10, "offset": 0, "filters": {"name": company.name}},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["data"][0]["name"] == company.name
