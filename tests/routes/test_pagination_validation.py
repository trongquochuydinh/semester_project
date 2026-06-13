import pytest


@pytest.mark.parametrize(
    "endpoint",
    [
        "/api/users/search",
        "/api/items/search",
        "/api/orders/search",
    ],
)
def test_paginated_endpoints_reject_invalid_limit(
    auth_client_factory,
    superadmin,
    endpoint,
):
    client = auth_client_factory(superadmin)

    response = client.post(endpoint, json={"limit": -1, "offset": 0})

    assert response.status_code == 422
