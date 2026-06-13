def test_paginate_companies_rejects_invalid_limit(auth_client_factory, superadmin):
    client = auth_client_factory(superadmin)

    response = client.post(
        "/api/companies/search",
        json={"limit": -1, "offset": 0},
    )

    assert response.status_code == 422


def test_paginate_companies_rejects_limit_above_max(auth_client_factory, superadmin):
    client = auth_client_factory(superadmin)

    response = client.post(
        "/api/companies/search",
        json={"limit": 1000, "offset": 0},
    )

    assert response.status_code == 422
