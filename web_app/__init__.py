from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os

# initialize Flask
app = Flask(__name__)

# configure app
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///site.db")
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev_secret")

# Example route
@app.route('/')
def init_home():
    return render_template('main.html')

# Only needed for local dev with `python -m web_app`
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
