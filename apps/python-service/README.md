# Python Microservice

A demonstration Python microservice built with Flask for GitHub Actions CI/CD demonstrations.

## Features

- RESTful API endpoints
- Health check endpoint for container orchestration
- Calculator API demonstrating request/response patterns
- Comprehensive test coverage
- Linting with pylint and flake8

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Development mode
flask --app app run --debug

# Production mode with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html
```

### Linting

```bash
# Run pylint
pylint app

# Run flake8
flake8 app
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service information |
| `/health` | GET | Health check |
| `/api/v1/items` | GET | List all items |
| `/api/v1/items/<id>` | GET | Get specific item |
| `/api/v1/calculate` | POST | Perform calculation |

## Project Structure

```
python-service/
├── app/
│   ├── __init__.py      # Application factory
│   └── routes.py        # API routes
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Pytest fixtures
│   └── test_routes.py   # Route tests
├── requirements.txt     # Dependencies
├── setup.py            # Package setup
└── README.md           # This file
```
