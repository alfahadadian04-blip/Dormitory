"""Dormitory Management System - Flask application entry point."""
import os
from datetime import date, datetime
from flask import Flask, redirect, url_for

from config import Config
from models import db, Admin
from auth import auth_bp, login_manager
from routes import main_bp


def create_app(config_class=Config) -> Flask:
    # On serverless platforms (Vercel, AWS Lambda) the project directory is
    # read-only; Flask's default instance_path (next to app.py) can't be
    # created there. Redirect it to /tmp, which is the only writable dir.
    instance_path = None
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        instance_path = "/tmp/flask_instance"
        os.makedirs(instance_path, exist_ok=True)

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        instance_path=instance_path,
    )
    app.config.from_object(config_class)

    # Extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Template helpers
    @app.template_filter("money")
    def money_filter(value):
        try:
            return f"{float(value):,.2f}"
        except (TypeError, ValueError):
            return "0.00"

    @app.template_filter("date_fmt")
    def date_fmt(value, fmt="%b %d, %Y"):
        if not value:
            return ""
        if isinstance(value, datetime):
            return value.strftime(fmt)
        if isinstance(value, date):
            return value.strftime(fmt)
        return str(value)

    @app.context_processor
    def inject_globals():
        return {"current_year": date.today().year}

    # Error handlers
    @app.errorhandler(404)
    def not_found(_e):
        from flask import render_template
        return render_template("error.html", code=404,
                               message="Page not found."), 404

    @app.errorhandler(500)
    def server_error(_e):
        from flask import render_template
        db.session.rollback()
        return render_template("error.html", code=500,
                               message="Something went wrong on our end."), 500

    # Root redirect
    @app.route("/home")
    def home():
        return redirect(url_for("main.dashboard"))

    # Initialize database and seed default admin.
    # Set SKIP_DB_INIT=true in production after the first deploy to avoid
    # re-running db.create_all() on every serverless cold start.
    if os.getenv("SKIP_DB_INIT", "").lower() not in ("1", "true", "yes"):
        with app.app_context():
            try:
                db.create_all()
                _seed_default_admin(app)
            except Exception as exc:  # noqa: BLE001 - surface init errors clearly
                app.logger.error("Database initialization failed: %s", exc)

    return app


def _seed_default_admin(app: Flask) -> None:
    """Create the default admin user if the admins table is empty."""
    if Admin.query.count() > 0:
        return
    username = app.config.get("DEFAULT_ADMIN_USERNAME", "adian")
    password = app.config.get("DEFAULT_ADMIN_PASSWORD", "adian123")
    admin = Admin(username=username)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    app.logger.info("Seeded default admin user: %s", username)


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_ENV", "production") == "development"
    host = os.getenv("HOST", "127.0.0.1")
    app.run(host=host, port=port, debug=debug)
