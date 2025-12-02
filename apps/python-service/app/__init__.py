"""
Python Microservice Application Package

This module initializes the Flask application for the Python microservice.
It demonstrates enterprise-grade patterns for GitHub Actions CI/CD.
"""

from flask import Flask


def create_app(config_name: str = "default") -> Flask:
    """
    Application factory pattern for Flask app creation.

    Args:
        config_name: Configuration environment name (default, development, testing, production)

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration based on environment
    app.config.from_mapping(
        SECRET_KEY="dev-secret-key",
        ENVIRONMENT=config_name,
    )

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
