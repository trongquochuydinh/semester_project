from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
import os

# initialize Flask
app = Flask(__name__)

# configure app
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "f1c893bfb0c4d2e3b6d79df8c1d05f4ed2b1c78d1a1e0f48c2ef54c4b8a9e89e")

# Example route
@app.route('/')
def init_home():
    return render_template('main.html')

# Only needed for local dev with `python -m web_app`
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
