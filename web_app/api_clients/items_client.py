from flask import session, jsonify
from web_app.api_clients.utils import api_post, api_get, APIClientError

def paginate_item(data):
    res = api_post("/api/items/paginate", data)
    return (res.text, res.status_code, res.headers.items())

def create_item(data):
    res = api_post("/api/items/create", data)
    return (res.text, res.status_code, res.headers.items())

def edit_item(item_id: int, data):
    try:
        res = api_post(f"/api/items/edit/{item_id}", data)
        resp_json = res.json()
        
        return jsonify({
                "success": True,
                "message": resp_json.get("message")
            })
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def toggle_user_is_active(item_id: int):
    """Disable item via API."""
    try:
        res = api_post(f"/api/items/toggle_item_is_active/{item_id}")
        return res.json()

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code    

def get_item(item_id):
    res = api_get(f"/api/items/get/{item_id}")
    return (res.text, res.status_code, res.headers.items())