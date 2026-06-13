def test_superadmin_can_edit_company(auth_client_factory, superadmin, company):
    client = auth_client_factory(superadmin)

    response = client.put(
        f"/api/companies/{company.id}",
        json={"name": "EditedCo", "field": "Finance"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Company was successfully updated."


def test_edit_company_duplicate_name_returns_409(
    auth_client_factory, superadmin, company, company2
):
    client = auth_client_factory(superadmin)

    response = client.put(
        f"/api/companies/{company.id}",
        json={"name": company2.name, "field": "X"},
    )

    assert response.status_code == 409
