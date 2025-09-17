import os

host = os.environ.get('DB_HOST')
dbname = os.environ.get('DB_NAME')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')

FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')