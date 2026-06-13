from api.utils.auth_utils import create_oauth_exchange_code, consume_oauth_exchange_code
from api.schemas import LoginResponse
from api.schemas.auth_schema import OAuthInfo


def test_exchange_oauth_code_returns_login_response():
    login_response = LoginResponse(
        access_token="test-token",
        token_type="bearer",
        id=1,
        username="testuser",
        role="admin",
        company_id=1,
        oauth_info=OAuthInfo(github=True),
    )
    code = create_oauth_exchange_code(login_response.model_dump())

    payload = consume_oauth_exchange_code(code)

    assert payload is not None
    assert payload["access_token"] == "test-token"
    assert payload["username"] == "testuser"


def test_exchange_oauth_code_is_single_use():
    login_response = LoginResponse(
        access_token="test-token",
        token_type="bearer",
        id=1,
        username="testuser",
        role="admin",
        oauth_info=OAuthInfo(),
    )
    code = create_oauth_exchange_code(login_response.model_dump())

    assert consume_oauth_exchange_code(code) is not None
    assert consume_oauth_exchange_code(code) is None


def test_oauth_exchange_endpoint(client):
    login_response = LoginResponse(
        access_token="test-token",
        token_type="bearer",
        id=1,
        username="testuser",
        role="admin",
        oauth_info=OAuthInfo(),
    )
    code = create_oauth_exchange_code(login_response.model_dump())

    response = client.post("/api/auth/oauth/exchange", json={"code": code})

    assert response.status_code == 200
    assert response.json()["access_token"] == "test-token"


def test_oauth_exchange_endpoint_rejects_invalid_code(client):
    response = client.post("/api/auth/oauth/exchange", json={"code": "invalid-code"})

    assert response.status_code == 400
