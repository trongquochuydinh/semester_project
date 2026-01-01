from flask import Flask, jsonify, session, request, redirect, url_for
from web_app.config import FLASK_SECRET_KEY
from web_app.api_clients.utils import APIUnauthorizedError

app = Flask(__name__)
app.config.update(
    SECRET_KEY=FLASK_SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False
)

@app.errorhandler(APIUnauthorizedError)
def handle_api_unauthorized(e):
    if request.is_json:
        return jsonify({"error": "Session expired"}), 401

    return redirect(url_for("auth.home"))

@app.route('/set_language')
def set_language():
    lang = request.args.get('lang')
    session['lang'] = lang
    return redirect(request.referrer or '/')

# --- Register blueprints ---
from web_app.routes.context import context_bp
from web_app.routes.auth import auth_bp
from web_app.routes.users import users_bp
from web_app.routes.companies import companies_bp
from web_app.routes.items import items_bp
from web_app.routes.orders import orders_bp

app.register_blueprint(context_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(companies_bp)
app.register_blueprint(items_bp)
app.register_blueprint(orders_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)