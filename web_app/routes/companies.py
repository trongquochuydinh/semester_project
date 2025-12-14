from flask import Blueprint, session, render_template, request
from web_app.routes.api_clients.utils import login_required, token_required
from web_app.routes.api_clients.companies_client import get_companies as proxy_get_companies, create_company as proxy_create_company, get_company as proxy_get_company

companies_bp = Blueprint('companies', __name__, url_prefix='/companies')

@companies_bp.route('/management')
def company_management():
    if session.get('user') is None:
        return render_template('login.html')
    return render_template('management_views/company_management.html')

@companies_bp.route('/create', methods=['POST'])
@token_required
def create_user():
    data = request.get_json()
    return proxy_create_company(data)

@companies_bp.route('/get_companies')
def get_companies():
    return proxy_get_companies()

@companies_bp.route("/get/<int:company_id>")
def get_company(company_id):
    return proxy_get_company(company_id)