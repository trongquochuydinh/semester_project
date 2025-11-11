import os
from flask import Flask, session, request, redirect
from config import SECRET_KEY

app = Flask(__name__)
app.config.update(
    SECRET_KEY=SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False
)

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
from web_app.routes.pagination import pagination_bp

app.register_blueprint(context_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(companies_bp)
app.register_blueprint(pagination_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)