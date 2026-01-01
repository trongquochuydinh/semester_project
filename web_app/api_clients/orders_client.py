from flask import session, jsonify
from web_app.api_clients.utils import api_post, api_get, APIClientError

def paginate_order(data):
    res = api_post("/api/orders/paginate", data)
    return (res.text, res.status_code, res.headers.items())
