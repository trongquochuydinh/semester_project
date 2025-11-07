import os
from flask import Flask, g, session, request, redirect
from web_app.localization.localization import Translator
from config import SECRET_KEY

# Initialize Flask app
app = Flask(__name__)

app.config.update(
    SECRET_KEY=SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False  # False for localhost
)

# Initialize translator
translator = Translator()

@app.before_request
def set_language_context():
    g.lang = session.get('lang', 'en')
    translator.set_language(g.lang)

@app.context_processor
def inject_translator():
    return dict(t=lambda key: translator.t(key))

@app.route('/set_language')
def set_language():
    lang = request.args.get('lang')
    session['lang'] = lang
    return redirect(request.referrer or '/')

# Register blueprints
from web_app.routes.auth import auth_bp
from web_app.routes.users import users_bp
from web_app.routes.companies import companies_bp
from web_app.routes.pagination import pagination_bp

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(companies_bp)
app.register_blueprint(pagination_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)


# TODO:

# fix hierarchy pagination for admin and superadmin
# dont rely on session['user']['role'] to display front end, instead fetch from backend API to ensure security
