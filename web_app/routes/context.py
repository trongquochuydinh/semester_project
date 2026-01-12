# Import Flask components for blueprint creation, global context, and session management
from flask import Blueprint, g, session

# Import custom localization module for multi-language support
from web_app.localization.localization import Translator

# Create Blueprint for global context management (no URL prefix - applies to all routes)
context_bp = Blueprint("context", __name__)

# Initialize global translator instance for handling internationalization
translator = Translator()

@context_bp.before_app_request
def load_global_context():
    """
    Set up global context variables before processing any request.
    This function runs before every request to establish user session data
    and language preferences that will be available throughout the application.
    """
    # --- Language setup ---
    # Get user's language preference from session, default to English
    g.lang = session.get("lang", "en")
    
    # Configure translator with user's preferred language
    translator.set_language(g.lang)

    # --- User context setup ---
    # Store user's role from session for authorization checks
    g.role = session.get("role")
    
    # Store user's company ID for multi-tenant data filtering
    g.company_id = session.get("company_id")


@context_bp.app_context_processor
def inject_globals():
    """
    Inject global variables and functions into all Jinja2 templates.
    These variables become available in every template without explicit passing.
    
    Returns:
        dict: Dictionary of global template variables and functions
    """
    return dict(
        # Translation function - allows templates to use {{ t('key') }} for localized text
        t=lambda key: translator.t(key),
        
        # User role - enables role-based conditional rendering in templates
        role=g.role,
        
        # Current language - useful for language-specific styling or logic
        lang=g.lang,
        
        # Company ID - enables company-specific template behavior
        company_id=g.company_id,
        
        # JavaScript translations - provides client-side access to translation data
        js_translations=translator.translations
    )