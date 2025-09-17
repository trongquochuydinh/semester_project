from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os

from web_app.utils.flask_utils import generate_flask_key

app = Flask(__name__)

@app.route('/')
def init_home():
    return render_template('main.html')

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev_secret")
    app.run()