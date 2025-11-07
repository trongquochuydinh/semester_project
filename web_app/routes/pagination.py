from flask import Blueprint, request, session, render_template
from web_app.routes.api_clients.users_client import users_table_data
from web_app.routes.api_clients.companies_client import companies_table_data

pagination_bp = Blueprint('pagination', __name__, url_prefix='/paginate')

@pagination_bp.route('', methods=['POST'])
def paginate_proxy():
    if session.get('user') is None:
        return render_template('main.html')

    data = request.get_json()
    data.setdefault('filters', {})
    data['filters']['user_role'] = session.get('user', {}).get('role')
    data['filters']['company_id'] = session.get('user', {}).get('company_id')

    if data.get('table_name') == 'users':
        return users_table_data(data)
    elif data.get('table_name') == 'companies':
        return companies_table_data(data)
