from flask import jsonify
from web_app.routes.api_clients.utils import api_get, APIClientError

def get_companies():
    """Fetch list of companies via the FastAPI backend."""
    try:
        res = api_get("/api/companies/get_companies")
        return (res.text, res.status_code, res.headers.items())

    except APIClientError as e:
        # graceful fallback — network or backend error
        return jsonify({"error": e.message}), e.status_code
