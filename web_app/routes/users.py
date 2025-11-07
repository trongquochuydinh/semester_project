from flask import Blueprint, request, session, render_template, jsonify
from web_app.routes.api_clients.users_client import users_table_data, create_user as proxy_create_user, get_roles as proxy_get_roles

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/management')
def user_management():
    if session.get('user') is None:
        return render_template('login.html')
    return render_template('management_views/user_management.html')

@users_bp.route('/create', methods=['POST'])
def create_user():
    if session.get('user') is None:
        return render_template('index.html')
    data = request.get_json()
    return proxy_create_user(data)

@users_bp.route('/get_roles')
def get_roles():
    return proxy_get_roles()
