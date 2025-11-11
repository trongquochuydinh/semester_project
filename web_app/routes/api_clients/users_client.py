from flask import session, jsonify
from web_app.routes.api_clients.utils import api_post, api_get, APIClientError


def send_login_request(identifier, password):
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
        }
        session["token"] = user_data["access_token"]

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
        user_role = get_role()
        if not user_role:
            return jsonify({"error": "Failed to determine user role"}), 403

        res = api_get("/api/users/get_subroles", params={"creator_role": user_role})
        return (res.text, res.status_code, res.headers.items())

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code


def get_role():
    """Fetch the user's role via FastAPI using stored JWT."""
    try:
        res = api_get("/api/users/get_my_role")

        if res.status_code == 200:
            data = res.json()
            return data.get("role")

    except APIClientError:
        pass
    except Exception:
        pass

    return None


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
    token = session.get("token")
    if not token:
        return jsonify({"error": "Not logged in"}), 401

    user_id = session.get("user", {}).get("id")
    if not user_id:
        return jsonify({"error": "Missing user ID"}), 400

    try:
        res = api_post("/api/users/logout", {"user_id": user_id})
        return (res.text, res.status_code, res.headers.items())

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def get_user_count():
    """Get total user count via API."""
    try:
        res = api_get("/api/users/get_user_stats")
        return res.json()

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code