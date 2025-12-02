"""
Route Tests for Python Microservice

This module contains comprehensive tests for all API endpoints.
Demonstrates pytest testing patterns for GitHub Actions demonstrations.
"""

import json
import pytest


class TestIndexRoute:
    """Tests for the index route (/)."""

    def test_index_returns_service_info(self, client):
        """Test that index returns service information."""
        response = client.get("/")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["service"] == "python-microservice"
        assert data["version"] == "1.0.0"
        assert data["status"] == "healthy"


class TestHealthRoute:
    """Tests for the health check route (/health)."""

    def test_health_returns_healthy_status(self, client):
        """Test that health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "checks" in data
        assert data["checks"]["database"] == "ok"
        assert data["checks"]["cache"] == "ok"


class TestItemsRoute:
    """Tests for the items routes (/api/v1/items)."""

    def test_get_items_returns_list(self, client):
        """Test that get items returns a list of items."""
        response = client.get("/api/v1/items")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) == 3
        assert data["total"] == 3

    def test_get_item_returns_single_item(self, client):
        """Test that get item returns a single item."""
        response = client.get("/api/v1/items/1")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["id"] == 1
        assert data["name"] == "Item 1"

    def test_get_item_not_found(self, client):
        """Test that get item returns 404 for non-existent item."""
        response = client.get("/api/v1/items/999")
        assert response.status_code == 404

        data = json.loads(response.data)
        assert "error" in data


class TestCalculateRoute:
    """Tests for the calculate route (/api/v1/calculate)."""

    def test_calculate_add(self, client):
        """Test addition operation."""
        response = client.post(
            "/api/v1/calculate",
            data=json.dumps({"a": 10, "b": 5, "operation": "add"}),
            content_type="application/json"
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["result"] == 15
        assert data["operation"] == "add"

    def test_calculate_subtract(self, client):
        """Test subtraction operation."""
        response = client.post(
            "/api/v1/calculate",
            data=json.dumps({"a": 10, "b": 5, "operation": "subtract"}),
            content_type="application/json"
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["result"] == 5

    def test_calculate_multiply(self, client):
        """Test multiplication operation."""
        response = client.post(
            "/api/v1/calculate",
            data=json.dumps({"a": 10, "b": 5, "operation": "multiply"}),
            content_type="application/json"
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["result"] == 50

    def test_calculate_divide(self, client):
        """Test division operation."""
        response = client.post(
            "/api/v1/calculate",
            data=json.dumps({"a": 10, "b": 5, "operation": "divide"}),
            content_type="application/json"
        )
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["result"] == 2

    def test_calculate_divide_by_zero(self, client):
        """Test division by zero returns error."""
        response = client.post(
            "/api/v1/calculate",
            data=json.dumps({"a": 10, "b": 0, "operation": "divide"}),
            content_type="application/json"
        )
        assert response.status_code == 400

        data = json.loads(response.data)
        assert "error" in data

    def test_calculate_invalid_operation(self, client):
        """Test invalid operation returns error."""
        response = client.post(
            "/api/v1/calculate",
            data=json.dumps({"a": 10, "b": 5, "operation": "invalid"}),
            content_type="application/json"
        )
        assert response.status_code == 400

        data = json.loads(response.data)
        assert "error" in data

    def test_calculate_no_data(self, client):
        """Test no data returns error."""
        response = client.post(
            "/api/v1/calculate",
            content_type="application/json"
        )
        assert response.status_code == 400


class TestPerformCalculation:
    """Tests for the perform_calculation function."""

    def test_perform_calculation_add(self):
        """Test perform_calculation with addition."""
        from app.routes import perform_calculation
        result = perform_calculation(10, 5, "add")
        assert result == 15

    def test_perform_calculation_subtract(self):
        """Test perform_calculation with subtraction."""
        from app.routes import perform_calculation
        result = perform_calculation(10, 5, "subtract")
        assert result == 5

    def test_perform_calculation_multiply(self):
        """Test perform_calculation with multiplication."""
        from app.routes import perform_calculation
        result = perform_calculation(10, 5, "multiply")
        assert result == 50

    def test_perform_calculation_divide(self):
        """Test perform_calculation with division."""
        from app.routes import perform_calculation
        result = perform_calculation(10, 5, "divide")
        assert result == 2

    def test_perform_calculation_invalid_operation(self):
        """Test perform_calculation with invalid operation."""
        from app.routes import perform_calculation
        with pytest.raises(ValueError):
            perform_calculation(10, 5, "invalid")

    def test_perform_calculation_divide_by_zero(self):
        """Test perform_calculation with division by zero."""
        from app.routes import perform_calculation
        with pytest.raises(ZeroDivisionError):
            perform_calculation(10, 0, "divide")
