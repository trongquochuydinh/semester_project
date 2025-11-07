from flask import request, session, jsonify
import requests

from config import API_URL

def send_login_request(identifier, password):
    api_url = f'{API_URL}/api/users/login'
    try:
        res = requests.post(api_url, json={'identifier': identifier, 'password': password})
        
        if res.status_code == 200:
            user_data = res.json()
            # Store only essential info in session
            session['user'] = {
                'id': user_data['id'],
                'username': user_data['username'],
            }
            session['token'] = user_data['access_token']

            return jsonify({'success': True, 'user': session['user']})
        
        else:
            # Pass through backend error messages when possible
            try:
                error = res.json()
            except Exception:
                error = {'detail': res.text}
            return jsonify({'error': error.get('detail', 'Login failed')}), res.status_code
    
    except Exception as e:
        return jsonify({'error': 'API connection failed', 'detail': str(e)}), 502
    
def users_table_data(data):
    api_url = f"{API_URL}/api/paginate"
    try:
        res = requests.post(api_url, json=data)
        return (res.text, res.status_code, res.headers.items())
    except Exception as e:
        return jsonify({'error': 'API connection failed', 'detail': str(e)}), 502
    
def get_subroles():
    if session.get('user') is None:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_role = session['user']['role']
    api_url = f"{API_URL}/api/users/get_subroles?creator_role={user_role}"
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

def logout_user():
    if session.get('user') is None:
        return jsonify({'error': 'Not logged in'}), 401
    
    user_id = session['user']['id']
    api_url = f"{API_URL}/api/users/logout"
    try:
        res = requests.post(api_url, json={'user_id': user_id})
        return (res.text, res.status_code, res.headers.items())
    except Exception as e:
        return jsonify({'error': 'API connection failed', 'detail': str(e)}), 502