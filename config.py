import os

host = os.environ.get('DB_HOST')
dbname = os.environ.get('DB_NAME')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')

API_URL = os.environ.get('API_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')