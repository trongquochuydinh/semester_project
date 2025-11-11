from flask import Blueprint, session, render_template
from web_app.routes.api_clients.companies_client import get_companies as proxy_get_companies

companies_bp = Blueprint('companies', __name__, url_prefix='/companies')

@companies_bp.route('/management')
def company_management():
    if session.get('user') is None:
        return render_template('login.html')
    return render_template('management_views/company_management.html')

@companies_bp.route('/get')
def get_companies():
    return proxy_get_companies()
