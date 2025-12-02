"""
Flask Routes Module

This module contains the route definitions for the Python microservice.
Demonstrates RESTful API patterns for GitHub Actions demonstrations.
"""

from flask import Blueprint, jsonify, request
from typing import Dict, Any

# Create the main blueprint
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index() -> Dict[str, str]:
    """
    Root endpoint returning service information.

    Returns:
        JSON response with service name and version
    """
    return jsonify({
        "service": "python-microservice",
        "version": "1.0.0",
        "status": "healthy"
    })


@main_bp.route("/health")
def health_check() -> Dict[str, str]:
    """
    Health check endpoint for container orchestration.

    Returns:
        JSON response with health status
    """
    return jsonify({
        "status": "healthy",
        "checks": {
            "database": "ok",
            "cache": "ok"
        }
    })


@main_bp.route("/api/v1/items", methods=["GET"])
def get_items() -> Dict[str, Any]:
    """
    Get all items endpoint.

    Returns:
        JSON response with list of items
    """
    items = [
        {"id": 1, "name": "Item 1", "description": "First item"},
        {"id": 2, "name": "Item 2", "description": "Second item"},
        {"id": 3, "name": "Item 3", "description": "Third item"},
    ]
    return jsonify({"items": items, "total": len(items)})


@main_bp.route("/api/v1/items/<int:item_id>", methods=["GET"])
def get_item(item_id: int) -> tuple:
    """
    Get a specific item by ID.

    Args:
        item_id: The ID of the item to retrieve

    Returns:
        JSON response with item data or 404 error
    """
    items = {
        1: {"id": 1, "name": "Item 1", "description": "First item"},
        2: {"id": 2, "name": "Item 2", "description": "Second item"},
        3: {"id": 3, "name": "Item 3", "description": "Third item"},
    }

    if item_id in items:
        return jsonify(items[item_id])
    return jsonify({"error": "Item not found"}), 404


@main_bp.route("/api/v1/calculate", methods=["POST"])
def calculate() -> tuple:
    """
    Perform a calculation based on input data.

    Expects JSON body with 'a', 'b', and 'operation' fields.

    Returns:
        JSON response with calculation result
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        a = float(data.get("a", 0))
        b = float(data.get("b", 0))
        operation = data.get("operation", "add")

        result = perform_calculation(a, b, operation)
        return jsonify({"result": result, "operation": operation})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except ZeroDivisionError:
        return jsonify({"error": "Division by zero is not allowed"}), 400


def perform_calculation(a: float, b: float, operation: str) -> float:
    """
    Perform arithmetic calculation.

    Args:
        a: First operand
        b: Second operand
        operation: Operation to perform (add, subtract, multiply, divide)

    Returns:
        Calculation result

    Raises:
        ValueError: If operation is not supported
        ZeroDivisionError: If dividing by zero
    """
    def safe_divide(x: float, y: float) -> float:
        """Divide with zero check."""
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return x / y

    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": safe_divide,
    }

    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}")

    return operations[operation](a, b)
