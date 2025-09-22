import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from config import FLASK_SECRET_KEY

from web_app.routes.users import send_login_request

# initialize Flask
app = Flask(__name__)

# configure app
app.config["SECRET_KEY"] = os.urandom(24)

# Example route
@app.route('/')
def init_home():
    return render_template('main.html')

@app.route('/admin/users')
def admin_users():

    if session.get('user') is None:
        return render_template('main.html')

    return render_template('admin_users.html')

@app.route('/login', methods=['POST'])
def login_proxy():
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')

    return send_login_request(identifier, password)

@app.route('/paginate', methods=['POST'])
def paginate_proxy():

    if session.get('user') is None:
        return render_template('main.html')

    data = request.get_json()

    # parse the data and determine which route it should use
    import requests
    from config import API_URL
    api_url = f"{API_URL}/api/paginate"
    try:
        res = requests.post(api_url, json=data)
        return (res.text, res.status_code, res.headers.items())
    except Exception as e:
        return jsonify({'error': 'API connection failed', 'detail': str(e)}), 502

# Only needed for local dev with `python -m web_app`
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)