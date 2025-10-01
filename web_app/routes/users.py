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
                'role': user_data['role'],
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
    
def get_roles():
    if session.get('user') is None:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_role = session['user']['role']   # e.g. "superadmin", "admin"
    api_url = f"{API_URL}/api/users/roles?creator_role={user_role}"
    try:
        res = requests.get(api_url)
        return (res.text, res.status_code, res.headers.items())
    except Exception as e:
        return jsonify({'error': 'API connection failed', 'detail': str(e)}), 502

def create_user(data):
    api_url = f"{API_URL}/api/users/create"
    try:
        res = requests.post(api_url, json=data)
        if res.status_code == 200:
            resp_json = res.json()
            return jsonify({
                'success': True,
                'message': resp_json.get('message'),
                'initial_password': resp_json.get('initial_password')
            })
        else:
            return (res.text, res.status_code, res.headers.items())
    except Exception as e:
        return jsonify({'error': 'API connection failed', 'detail': str(e)}), 502