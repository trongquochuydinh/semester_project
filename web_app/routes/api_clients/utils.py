from flask import jsonify, session, render_template
from functools import wraps
import requests
from config import API_URL

class APIClientError(Exception):
    def __init__(self, message, status_code=502):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class APIUnauthorizedError(APIClientError):
    pass

def api_request(method, endpoint, data=None, params=None):
    url = f"{API_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}

    token = session.get("token")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        res = requests.request(
            method.upper(),
            url,
            json=data,
            params=params,
            headers=headers,
            timeout=5
        )

        if res.status_code == 401:
            session.pop("token", None)
            session.pop("user", None)

            raise APIUnauthorizedError("Session expired", 401)

        # Other errors
        if res.status_code >= 400:
            try:
                detail = res.json().get("detail", res.text)
            except Exception:
                detail = res.text
            raise APIClientError(detail, res.status_code)

        return res
    except APIUnauthorizedError:
        raise
    except requests.RequestException as e:
        raise APIClientError(str(e), 502)

def api_get(endpoint, params=None):
    return api_request("get", endpoint, params=params)

def api_post(endpoint, data=None):
    return api_request("post", endpoint, data=data)

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if session.get("user") is None and session.get("token") is None:
            return render_template("login.html")
        return view_func(*args, **kwargs)
    return wrapper


def token_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        token = session.get("token")
        if not token:
            return jsonify({"error": "Not logged in"}), 401
        return view_func(*args, **kwargs)
    return wrapper
