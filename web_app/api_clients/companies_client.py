from flask import jsonify
from web_app.api_clients.utils import api_get, api_post, APIClientError

def get_companies():
    """Fetch list of companies via the FastAPI backend."""
    try:
        res = api_get("/api/companies/get_companies")
        return (res.text, res.status_code, res.headers.items())
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code
    
def create_company(data):
    try:
        res = api_post("/api/companies/create", data)
        return (res.text, res.status_code, res.headers.items())
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code
    
def edit_company(company_id: int, data):
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
    try:
        res = api_post(f"/api/companies/delete/{company_id}")
        resp_json = res.json()
        return jsonify({
            "success": True,
            "message": resp_json.get("message")
        })
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

def get_company(company_id):
    try:
        res = api_get(f"/api/companies/get/{company_id}")
        return (res.text, res.status_code, res.headers.items())
    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code
    
def paginate_company(data):
    res = api_post("/api/companies/paginate", data)
    return (res.text, res.status_code, res.headers.items())
