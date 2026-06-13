def test_github_login_redirect_url(client_with_db):
    response = client_with_db.get("/api/auth/github/login")

    assert response.status_code == 200
    assert "redirect_url" in response.json()
