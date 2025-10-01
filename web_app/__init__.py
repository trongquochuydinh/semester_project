import os
from flask import Flask, render_template, g, request, redirect, url_for, session, jsonify, Blueprint

from web_app.routes.users import send_login_request, users_table_data, create_user as proxy_create_user, get_roles as proxy_get_roles
from web_app.routes.companies import get_companies as proxy_get_companies
from web_app.localization.localization import Translator

# initialize Flask
app = Flask(__name__)

# configure app
app.config["SECRET_KEY"] = os.urandom(24)

translator = Translator()

@app.route('/set_language')
def set_language():
    lang = request.args.get('lang')
    session['lang'] = lang
    return redirect(request.referrer or '/')

@app.before_request
def set_language_context():
    g.lang = session.get('lang', 'en')
    translator.set_language(g.lang)
    # Set default user if not already in session
    if 'user' not in session:
        session['user'] = {
            'id': 1,
            'username': 'test_user',
            'email': 'test_user@example.com',
            'role': 'superadmin'
        }

@app.context_processor
def inject_translator():
    return dict(t=lambda key: translator.t(key))

@app.route('/')
def init_home():
    if session.get('user') is None:
        return render_template('login.html')

    return render_template('index.html')

@app.route('/user_management')
def user_management():

    if session.get('user') is None:
        return render_template('login.html')

    return render_template('user_management.html')

@app.route('/login', methods=['POST'])
def login_proxy():
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')

    return send_login_request(identifier, password)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    if session.get('user') is None:
        return render_template('index.html')

    if request.method == 'POST':
        data = request.get_json()
        return proxy_create_user(data)
    return '', 405

@app.route("/get_roles")
def get_roles():
    return proxy_get_roles()

@app.route("/get_companies")
def get_companies():
    return proxy_get_companies()

@app.route('/paginate', methods=['POST'])
def paginate_proxy():

    if session.get('user') is None:
        return render_template('main.html')

    data = request.get_json()
    # Ensure filters is a dict and add user_role
    if "filters" not in data or not isinstance(data["filters"], dict):
        data["filters"] = {}
    data["filters"]["user_role"] = session.get('user', {}).get('role', None)
    data["filters"]["company_id"] = session.get('user', {}).get('company_id', None)
    # parse the data and determine which route it should use
    if data.get("table_name") == "users":
        return users_table_data(data)

# Only needed for local dev with `python -m web_app`
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)