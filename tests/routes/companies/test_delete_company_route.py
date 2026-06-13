def test_superadmin_can_delete_company(auth_client_factory, superadmin, company):
    client = auth_client_factory(superadmin)

    response = client.delete(f"/api/companies/{company.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Company was successfully deleted."


def test_delete_company_not_found(auth_client_factory, superadmin):
    client = auth_client_factory(superadmin)

    response = client.delete("/api/companies/9999")

    assert response.status_code == 404
