from flask import Blueprint, request, render_template
from web_app.api_clients.utils import login_required, token_required
from web_app.api_clients.users_client import(
    create_user as proxy_create_user, 
    get_subroles as proxy_get_subroles, 
    get_user_count as proxy_get_user_count, 
    get_user as proxy_get_user, 
    get_my_data as proxy_get_my_data,
    edit_user as proxy_edit_user,
    toggle_user_is_active as proxy_toggle_user_is_active,
    paginate_user as proxy_paginate_user
)

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/management')
@login_required
def user_management():
    return render_template('management_views/user_management.html')

@users_bp.route('/create', methods=['POST'])
@token_required
def create_user():
    data = request.get_json()
    return proxy_create_user(data)

@users_bp.route("/get_my_data")
@token_required
def get_my_data():
    return proxy_get_my_data()

@users_bp.route('/get_subroles')
@token_required
def get_subroles():
    return proxy_get_subroles()

@users_bp.route('/get_user_stats')
@token_required
def get_user_count():
    return proxy_get_user_count()

@users_bp.route("/get/<int:user_id>")
@token_required
def get_user(user_id):
    return proxy_get_user(user_id)

@users_bp.route("/edit/<int:user_id>", methods=["POST"])
@token_required
def edit_user(user_id):
    data = request.get_json()
    return proxy_edit_user(user_id, data)

@users_bp.route("/toggle_user_is_active/<int:user_id>", methods=["POST"])
@token_required
def disable_user(user_id):
    return proxy_toggle_user_is_active(user_id)

@users_bp.route("/paginate", methods=["POST"])
@token_required
def paginate_user():
    data = request.get_json() or {}
    return proxy_paginate_user(data)

# for frontend template rendering, check "user" in session
# for calls to API endpoints, check "token" in session