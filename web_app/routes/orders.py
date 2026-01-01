from flask import Blueprint, session, render_template, request
from web_app.api_clients.utils import token_required, login_required
from web_app.api_clients.orders_client import (
    paginate_order as proxy_paginate_order
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