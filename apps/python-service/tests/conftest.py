"""
Pytest Configuration and Fixtures

This module provides pytest fixtures for testing the Flask application.
Demonstrates testing patterns for GitHub Actions CI/CD.
"""

import pytest
from app import create_app


@pytest.fixture
def app():
    """
    Create application instance for testing.

    Yields:
        Flask: Configured Flask application in testing mode
    """
    app = create_app("testing")
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def client(app):
    """
    Create test client for the Flask application.

    Args:
        app: Flask application fixture

    Returns:
        FlaskClient: Test client for making HTTP requests
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create CLI runner for testing Flask commands.

    Args:
        app: Flask application fixture

    Returns:
        FlaskCliRunner: CLI test runner
    """
    return app.test_cli_runner()
