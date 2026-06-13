from flask import jsonify
from web_app.api_clients.utils import api_get, api_post, api_put, api_patch, APIClientError


def paginate_item(data):
    res = api_post("/api/items/search", data)
    return (res.text, res.status_code, res.headers.items())


def create_item(data):
    try:
        res = api_post("/api/items", data)
        resp_json = res.json()
        return jsonify({
            "success": True,
            "message": resp_json.get("message"),
        })
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code


def edit_item(item_id: int, data):
    try:
        res = api_put(f"/api/items/{item_id}", data)
        resp_json = res.json()
        return jsonify({
            "success": True,
            "message": resp_json.get("message", "Item updated"),
        })
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code


def toggle_item_is_active(item_id: int):
    try:
        res = api_patch(f"/api/items/{item_id}/status")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code


def get_item(item_id):
    res = api_get(f"/api/items/{item_id}")
    return (res.text, res.status_code, res.headers.items())
