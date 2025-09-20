from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
import os
import requests

from config import FLASK_SECRET_KEY

# initialize Flask
app = Flask(__name__)

# configure app
app.config["SECRET_KEY"] = FLASK_SECRET_KEY

# Example route
@app.route('/')
def init_home():
    return render_template('main.html')

@app.route('/login', methods=['POST'])
def login_proxy():
    data = request.get_json()
    identifier = data.get('identifier')
    password = data.get('password')
    api_url = 'http://localhost:8500/api/login'
    try:
        res = requests.post(api_url, json={'identifier': identifier, 'password': password})
        if res.status_code == 200:
            user_data = res.json()
            session['user'] = {
                'id': user_data['id'],
                'username': user_data['username'],
                'email': user_data['email'],
                'roles': user_data['roles'],
                'company_id': user_data.get('company_id')
            }
            return jsonify({'success': True, 'user': user_data})
        else:
            return (res.text, res.status_code, res.headers.items())
    except Exception as e:
        return jsonify({'error': 'API connection failed', 'detail': str(e)}), 502

# Only needed for local dev with `python -m web_app`
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)