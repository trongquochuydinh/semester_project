import os

API_URL = os.environ.get('API_URL')
FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
CANONICAL_HOST = os.environ.get('CANONICAL_HOST', "localhost:8000")