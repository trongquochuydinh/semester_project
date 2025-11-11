from flask import Blueprint, request, render_template
from web_app.routes.api_clients.utils import login_required, token_required
from web_app.routes.api_clients.users_client import create_user as proxy_create_user, get_role as proxy_get_role, get_subroles as proxy_get_subroles

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

@users_bp.route('/get_role')
@token_required
def get_role():
    return proxy_get_role()

@users_bp.route('/get_subroles')
@token_required
def get_subroles():
    return proxy_get_subroles()

# for frontend template rendering, check "user" in session
# for calls to API endpoints, check "token" in session