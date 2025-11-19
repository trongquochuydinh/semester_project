from flask import Blueprint, g, session
from web_app.localization.localization import Translator
from web_app.routes.api_clients.users_client import get_role

context_bp = Blueprint("context", __name__)

translator = Translator()

@context_bp.before_app_request
def load_global_context():
    # --- Language setup
    g.lang = session.get("lang", "en")
    translator.set_language(g.lang)

    g.role = session.get("role")
    g.company_id = session.get("company_id")


@context_bp.app_context_processor
def inject_globals():
    """Inject translator and role into all templates."""
    return dict(
        t=lambda key: translator.t(key),
        role=g.role,
        lang=g.lang,
        company_id=g.company_id,
    )
