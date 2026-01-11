from flask import Blueprint, abort, redirect, request, session, render_template
from web_app.api_clients.users_client import (
    login_user as proxy_login_user, 
    login_github as proxy_login_github,
    logout_user as proxy_logout_user,
    link_github as proxy_link_github,
    oauth_login_success
)
from web_app.api_clients.utils import api_get

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    error = request.args.get("error")
    if session.get('user') is None:
        return render_template(
            'auth_views/login.html',
            error=error
        )

    return render_template('base_views/index.html', error=error)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')
    return proxy_login_user(identifier, password)

@auth_bp.route("/auth/oauth-linked")
@auth_bp.route("/auth/oauth-success")
def oauth_success():
    token = request.args.get("token")
    oauth_login_success(token)

    return redirect("/")

@auth_bp.route("/auth/github/link")
def link_github():
    return proxy_link_github()

@auth_bp.route("/auth/github/login")
def github_login():
    return redirect(proxy_login_github())

@auth_bp.route('/logout')
def logout():
    if session.get('user'):
        try:
            proxy_logout_user()
        except Exception as e:
            print(f"Error updating user status: {e}")
    session.clear()
    return render_template('auth_views/login.html')
