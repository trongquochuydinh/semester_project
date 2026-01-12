# Import Flask JSON utilities for response formatting
from flask import jsonify
# Import API communication utilities and error handling
from web_app.api_clients.utils import api_get, api_post, APIClientError

# --- Company Data Retrieval Functions ---

def get_companies():
    """
    Fetch complete list of companies from the backend API.
    Returns all company records without pagination.
    
    Returns:
        tuple: (response_text, status_code, headers) for direct Flask response
        OR jsonify: Error response with message and status code
        
    Used for: Dropdown lists, selection interfaces, company overviews
    """
    try:
        res = api_get("/api/companies/get_companies")
        # Return raw response data for client processing
        return (res.text, res.status_code, res.headers.items())
    except APIClientError as e:
        # Return standardized JSON error response
        return jsonify({"error": e.message}), e.status_code

def get_company(company_id):
    """
    Fetch detailed information for a specific company.
    
    Args:
        company_id (int): Unique identifier of the company to retrieve
        
    Returns:
        tuple: (response_text, status_code, headers) containing company details
        OR jsonify: Error response if company not found or access denied
    """
    try:
        res = api_get(f"/api/companies/get/{company_id}")
        return (res.text, res.status_code, res.headers.items())
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def paginate_company(data):
    """
    Get paginated list of companies with filtering and sorting options.
    
    Args:
        data (dict): Pagination parameters including:
            - page (int): Page number to retrieve
            - size (int): Number of records per page
            - filters (dict): Search/filter criteria
            - sort (dict): Sorting preferences
            
    Returns:
        tuple: (response_text, status_code, headers) with paginated results
        
    Used for: Large company lists in management interfaces
    """
    res = api_post("/api/companies/paginate", data)
    return (res.text, res.status_code, res.headers.items())

# --- Company Management Functions ---

def create_company(data):
    """
    Create a new company record in the system.
    
    Args:
        data (dict): Company information including:
            - name (str): Company name
            - address (str): Business address
            - contact_info (dict): Email, phone, etc.
            - industry (str): Business sector
            - other company-specific fields
            
    Returns:
        tuple: (response_text, status_code, headers) with creation result
        OR jsonify: Error response if validation fails or creation error
    """
    try:
        res = api_post("/api/companies/create", data)
        return (res.text, res.status_code, res.headers.items())
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def edit_company(company_id: int, data):
    """
    Update existing company information.
    
    Args:
        company_id (int): Unique identifier of company to update
        data (dict): Updated company data (partial updates supported)
        
    Returns:
        jsonify: Success response with confirmation message
        OR jsonify: Error response if update fails or access denied
        
    Note: Returns formatted JSON response instead of raw API response
    """
    try:
        res = api_post(f"/api/companies/edit/{company_id}", data)
        resp_json = res.json()
        return jsonify({
            "success": True,
            "message": resp_json.get("message")
        })
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def delete_company(company_id):
    """
    Remove a company from the system.
    
    Args:
        company_id (int): Unique identifier of company to delete
        
    Returns:
        jsonify: Success response with confirmation message
        OR jsonify: Error response if deletion fails
        
    Warning: This may be a hard delete that affects related data.
    Ensure proper authorization and cascade handling in backend.
    """
    try:
        res = api_post(f"/api/companies/delete/{company_id}")
        resp_json = res.json()
        return jsonify({
            "success": True,
            "message": resp_json.get("message")
        })
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code
