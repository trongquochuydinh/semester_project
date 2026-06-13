from flask import jsonify
from web_app.api_clients.utils import api_get, api_post, APIClientError


def paginate_order(data):
    res = api_post("/api/orders/search", data)
    return (res.text, res.status_code, res.headers.items())


def paginate_order_items(order_id, data):
    res = api_post(f"/api/orders/{order_id}/items/search", data)
    return (res.text, res.status_code, res.headers.items())


def orders_this_week():
    try:
        res = api_get("/api/orders/stats")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code


def create_order(data):
    try:
        res = api_post("/api/orders", data)
        resp_json = res.json()
        return jsonify({
            "success": True,
            "message": resp_json.get("message"),
        })
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code


def cancel_order(order_id: int):
    try:
        res = api_post(f"/api/orders/{order_id}/cancel")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code


def complete_order(order_id: int):
    try:
        res = api_post(f"/api/orders/{order_id}/complete")
        return res.json()
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code
