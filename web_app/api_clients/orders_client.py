from flask import jsonify
from web_app.api_clients.utils import api_post, api_get, APIClientError


def paginate_order(data):
    res = api_post("/api/orders/paginate", data)
    return (res.text, res.status_code, res.headers.items())

def paginate_order_items(order_id, data):
    res = api_post(f"/api/orders/{order_id}/items/paginate", data)
    return (res.text, res.status_code, res.headers.items())

def create_order(data):
    try:
        res = api_post("/api/orders/create", data)
        resp_json = res.json()

        return jsonify({
            "success": True,
            "message": resp_json.get("message")
        })

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code


def cancel_order(order_id: int):
    try:
        res = api_post(f"/api/orders/cancel/{order_id}")
        return res.json()

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code
    
def complete_order(order_id: int):
    try:
        res = api_post(f"/api/orders/complete/{order_id}")
        return res.json()

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code
    
def orders_this_week():
    try:
        res = api_get("/api/orders/order_counts")
        return res.json()

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code
