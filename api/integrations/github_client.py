import requests
from api.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

def exchange_code_for_token(code: str) -> str:
    res = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        },
    )
    res.raise_for_status()
    return res.json()["access_token"]


def fetch_user(access_token: str) -> dict:
    res = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
    )
    res.raise_for_status()
    return res.json()
