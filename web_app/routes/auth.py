from flask import Blueprint, request, session, render_template
from web_app.api_clients.users_client import send_login_request, logout_user as proxy_logout_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    if session.get('user') is None:
        return render_template('login.html')
    return render_template('index.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')
    return send_login_request(identifier, password)

@auth_bp.route('/logout')
def logout():
    if session.get('user'):
        try:
            proxy_logout_user()
        except Exception as e:
            print(f"Error updating user status: {e}")
    session.clear()
    return render_template('login.html')
