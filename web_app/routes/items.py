from flask import Blueprint, session, render_template, request
from web_app.api_clients.utils import token_required, login_required
from web_app.api_clients.items_client import (
    paginate_item as proxy_paginate_item
)

items_bp = Blueprint('items', __name__, url_prefix='/items')

@items_bp.route('/management')
@login_required
def item_management():
    if session.get('user') is None:
        return render_template('auth_views/login.html')
    return render_template('management_views/item_management.html')

@items_bp.route("/paginate", methods=["POST"])
@token_required
def paginate_item():
    data = request.get_json() or {}
    return proxy_paginate_item(data)