from flask import request, session, jsonify
import requests

from config import API_URL

def get_companies():
    api_url = f"{API_URL}/api/companies/get_companies"
    try:
        res = requests.get(api_url)
        return (res.text, res.status_code, res.headers.items())
    except Exception as e:
        return jsonify({'error': 'API connection failed', 'detail': str(e)}), 502