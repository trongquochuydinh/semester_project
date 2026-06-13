import os

APP_ENV = os.getenv("APP_ENV", "development")
IS_PRODUCTION = APP_ENV == "production"

API_URL = os.environ.get("API_URL")
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
CANONICAL_HOST = os.environ.get("CANONICAL_HOST", "localhost:8000")


def validate_config() -> None:
    if IS_PRODUCTION:
        missing = []
        if not FLASK_SECRET_KEY:
            missing.append("FLASK_SECRET_KEY")
        if not API_URL:
            missing.append("API_URL")
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
