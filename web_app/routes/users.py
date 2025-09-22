from flask import request, session, jsonify
import requests

from config import API_URL

def send_login_request(identifier, password):
    api_url = f'{API_URL}/api/users/login'
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
    
def users_table_data(data):
    api_url = f"{API_URL}/api/paginate"
    try:
        res = requests.post(api_url, json=data)
        return (res.text, res.status_code, res.headers.items())
    except Exception as e:
        return jsonify({'error': 'API connection failed', 'detail': str(e)}), 502