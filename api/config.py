import logging
import os

logger = logging.getLogger(__name__)

APP_ENV = os.getenv("APP_ENV", "development")
IS_PRODUCTION = APP_ENV == "production"

host = os.environ.get("DB_HOST")
dbname = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")

_DEV_JWT_SECRET = "dev-secret-key"
JWT_SECRET = os.getenv("JWT_SECRET") or (_DEV_JWT_SECRET if not IS_PRODUCTION else None)
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")


def validate_config() -> None:
    if IS_PRODUCTION:
        required = {
            "JWT_SECRET": JWT_SECRET,
            "GITHUB_CLIENT_ID": GITHUB_CLIENT_ID,
            "GITHUB_CLIENT_SECRET": GITHUB_CLIENT_SECRET,
            "GITHUB_REDIRECT_URI": GITHUB_REDIRECT_URI,
            "DB_HOST": host,
            "DB_NAME": dbname,
            "DB_USER": user,
            "DB_PASSWORD": password,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
        if JWT_SECRET == _DEV_JWT_SECRET:
            raise RuntimeError("JWT_SECRET must not use the development default in production")
    elif not os.getenv("JWT_SECRET"):
        logger.warning(
            "JWT_SECRET is not set; using development default. "
            "Set JWT_SECRET before deploying."
        )
