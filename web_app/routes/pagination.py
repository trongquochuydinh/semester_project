from flask import Blueprint, request, jsonify
from web_app.routes.api_clients.utils import api_post, APIClientError, login_required, token_required

pagination_bp = Blueprint("pagination", __name__, url_prefix="/paginate")


@pagination_bp.route("", methods=["POST"])
@token_required
@login_required
def paginate_proxy():
    """Handle pagination requests for users, companies, etc."""
    try:
        data = request.get_json() or {}
        data.setdefault("filters", {})

        res = api_post("/api/paginate", data)
        return (res.text, res.status_code, res.headers.items())

    except APIClientError as e:
        return jsonify({"error": e.message}), e.status_code

    except Exception as e:
        return jsonify({"error": "Unexpected pagination error", "detail": str(e)}), 500
