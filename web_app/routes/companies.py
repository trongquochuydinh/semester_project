# Import Flask components for web routing, session management, and request handling
from flask import Blueprint, session, render_template, request

# Import custom authentication decorators for route protection
from web_app.api_clients.utils import token_required, login_required

# Import company-related API client functions with proxy naming to avoid conflicts
from web_app.api_clients.companies_client import (
    get_companies as proxy_get_companies,           # Fetch all companies list
    create_company as proxy_create_company,         # Company creation functionality
    get_company as proxy_get_company,               # Fetch individual company data
    edit_company as proxy_edit_company,             # Update company information
    delete_company as proxy_delete_company,         # Remove company from system
    paginate_company as proxy_paginate_company      # Get paginated company list
)

# Create Blueprint for company-related routes with '/companies' URL prefix
companies_bp = Blueprint('companies', __name__, url_prefix='/companies')

# --- Frontend Template Routes ---

@companies_bp.route('/management')
@login_required  # Requires user to be logged in (session-based auth)
def company_management():
    """
    Render the company management interface page.
    This is a frontend template route for administrative company management.
    """
    # Double-check session validity before rendering management interface
    if session.get('user') is None:
        return render_template('auth_views/login.html')  # Fallback to login if session invalid
    
    # Render company management dashboard for authenticated users
    return render_template('management_views/company_management.html')

# --- API Endpoints ---

@companies_bp.route('/create', methods=['POST'])
@token_required  # Requires valid API token for access
def create_company():
    """
    Create a new company.
    Accepts JSON payload with company details (name, address, contact info, etc.).
    """
    data = request.get_json()  # Extract JSON data from request body
    return proxy_create_company(data)  # Forward request to API client

@companies_bp.route('/get_companies')
@token_required  # Requires valid API token for access
def get_companies():
    """
    Fetch list of all companies in the system.
    Returns complete company data without pagination.
    Useful for dropdown lists and selection interfaces.
    """
    return proxy_get_companies()  # Forward request to API client

@companies_bp.route("/get/<int:company_id>")
@token_required  # Requires valid API token for access
def get_company(company_id):
    """
    Fetch details for a specific company by ID.
    
    Args:
        company_id (int): The unique identifier of the company to retrieve
    """
    return proxy_get_company(company_id)

@companies_bp.route("/edit/<int:company_id>", methods=["POST"])
@token_required  # Requires valid API token for access
def edit_company(company_id):
    """
    Update an existing company's information.
    
    Args:
        company_id (int): The unique identifier of the company to update
    Accepts JSON payload with updated company data.
    """
    data = request.get_json()  # Extract JSON data from request body
    return proxy_edit_company(company_id, data)  # Forward to API client with ID and data

@companies_bp.route("/delete/<int:company_id>", methods=["POST"])
@token_required  # Requires valid API token for access
def delete_company(company_id):
    """
    Remove a company from the system.
    
    Args:
        company_id (int): The unique identifier of the company to delete
    This is typically a hard delete - use with caution as it may affect related data.
    """
    return proxy_delete_company(company_id)  # Forward deletion request to API client

@companies_bp.route("/paginate", methods=["POST"])
@token_required  # Requires valid API token for access
def paginate_company():
    """
    Get paginated list of companies with optional filtering and sorting.
    Accepts JSON payload with pagination parameters (page, size, filters, search terms, etc.).
    Returns structured response with company data and pagination metadata.
    Used for large company lists in management interfaces.
    """
    data = request.get_json() or {}  # Get JSON data or empty dict if none provided
    return proxy_paginate_company(data)  # Forward request to API client