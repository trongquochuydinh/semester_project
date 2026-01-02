from flask import Blueprint, session, render_template, request
from web_app.api_clients.utils import token_required, login_required
from web_app.api_clients.orders_client import (
    paginate_order as proxy_paginate_order,
    paginate_order_items as proxy_paginate_order_items,
    create_order as proxy_create_order,
    cancel_order as proxy_cancel_order,
    complete_order as proxy_complete_order
)

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/management')
@login_required
@token_required
def order_management():
    if session.get('user') is None:
        return render_template('auth_views/login.html')
    return render_template('management_views/order_management.html')

@orders_bp.route("/paginate", methods=["POST"])
@token_required
def paginate_order():
    data = request.get_json() or {}
    return proxy_paginate_order(data)

@orders_bp.route("<int:order_id>/items/paginate", methods=["POST"])
@token_required
def paginate_order_items(order_id: int):
    data = request.get_json() or {}
    return proxy_paginate_order_items(order_id, data)

@orders_bp.route("/create", methods=["POST"])
@token_required
def create_order():
    data = request.get_json() or {}
    return proxy_create_order(data)

@orders_bp.route("/cancel/<int:order_id>", methods=["POST"])
@token_required
def cancel_order(order_id: int):
    return proxy_cancel_order(order_id)

@orders_bp.route("/complete/<int:order_id>", methods=["POST"])
@token_required
def complete_order(order_id: int):
    return proxy_complete_order(order_id)