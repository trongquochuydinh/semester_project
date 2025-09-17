from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
import os

from config import FLASK_SECRET_KEY

# initialize Flask
app = Flask(__name__)

# configure app
app.config["SECRET_KEY"] = FLASK_SECRET_KEY

# Example route
@app.route('/')
def init_home():
    return render_template('main.html')

# Only needed for local dev with `python -m web_app`
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
