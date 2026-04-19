"""Application configuration loaded from environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()


def _normalize_db_url(url: str) -> str:
    """Supabase/Heroku-style URLs sometimes come as postgres:// which SQLAlchemy
    no longer supports. Force the modern postgresql:// scheme."""
    if not url:
        return url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # Database
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(
        os.getenv("DATABASE_URL", "sqlite:///dorm.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Keep pooled connections healthy on Supabase (it closes idle ones)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Default admin credentials (used only to seed first admin)
    DEFAULT_ADMIN_USERNAME = os.getenv("DEFAULT_ADMIN_USERNAME", "adian")
    DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD", "adian123")

    # Feature flags
    ENABLE_ANALYTICS_DASHBOARD = os.getenv("ENABLE_ANALYTICS_DASHBOARD", "false").lower() == "true"
