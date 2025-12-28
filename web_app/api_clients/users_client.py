from flask import session, jsonify
from web_app.api_clients.utils import api_post, api_get, APIClientError


def login_user(identifier, password):
    """Authenticate the user and store session/token on success."""
    try:
        res = api_post("/api/users/login", {
            "identifier": identifier,
            "password": password
        })

        user_data = res.json()
        session["user"] = {
            "id": user_data["id"],
            "username": user_data["username"],
            "role": user_data["role"]
        }
        session["token"] = user_data["access_token"]
        session["role"] = user_data["role"]
        session["company_id"] = user_data["company_id"]

        return jsonify({"success": True, "user": session["user"]})

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

    except Exception as e:
        return jsonify({
            "error": "Unexpected client error",
            "detail": str(e)
        }), 500


def get_subroles():
    """Get allowed subroles for the current user."""
    try:
        res = api_get("/api/users/get_subroles")
        return (res.text, res.status_code, res.headers.items())

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def get_my_data():
    try:
        res = api_get("/api/users/me")

        return res.json()
        
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def create_user(data):
    """Create a new user via API."""
    try:
        res = api_post("/api/users/create", data)
        resp_json = res.json()

        return jsonify({
            "success": True,
            "message": resp_json.get("message"),
            "initial_password": resp_json.get("initial_password")
        })

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code


def logout_user():
    """Logout the current user by invalidating their session and updating backend."""
    try:
        res = api_post("/api/users/logout")
        return (res.text, res.status_code, res.headers.items())

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def get_user(user_id):
    """Get user details via API."""
    try:
        res = api_get(f"/api/users/get/{user_id}")
        return res.json()

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def get_user_count():
    """Get total user count via API."""
    try:
        res = api_get("/api/users/get_user_stats")
        return res.json()

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code
    
def edit_user(user_id, data):
    try:
        res = api_post(f"/api/users/edit_user/{user_id}", data)
        resp_json = res.json()

        return jsonify({
            "success": True,
            "message": resp_json.get("message")
        })
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code
    
def toggle_user_is_active(user_id):
    """Disable user via API."""
    try:
        res = api_post(f"/api/users/toggle_user_is_active/{user_id}")
        return res.json()

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def paginate_user(data):
    res = api_post("/api/users/paginate", data)
    return (res.text, res.status_code, res.headers.items())