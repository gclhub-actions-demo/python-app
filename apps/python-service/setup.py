"""
Setup script for Python Microservice.

This setup.py demonstrates enterprise packaging patterns for Python applications.
It can be used to build wheel distributions for deployment.

Usage:
    pip install -e .           # Install in development mode
    python setup.py sdist      # Create source distribution
    python setup.py bdist_wheel # Create wheel distribution
"""

from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

# Separate production and dev dependencies
prod_requirements = [r for r in requirements if not any(
    dev in r.lower() for dev in ["pytest", "pylint", "flake8", "mypy", "bandit", "safety"]
)]

dev_requirements = [r for r in requirements if any(
    dev in r.lower() for dev in ["pytest", "pylint", "flake8", "mypy", "bandit", "safety"]
)]

setup(
    # Package metadata
    name="python-microservice",
    version="1.0.0",
    author="GitHub Actions Demo Team",
    author_email="demo@example.com",
    description="A demonstration Python microservice for GitHub Actions CI/CD",
    long_description=open("README.md", "r", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/example/github-actions-demo",

    # Package configuration
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.11",

    # Dependencies
    install_requires=prod_requirements,
    extras_require={
        "dev": dev_requirements,
        "test": [r for r in dev_requirements if "pytest" in r.lower()],
        "lint": [r for r in dev_requirements if any(l in r.lower() for l in ["pylint", "flake8"])],
    },

    # Entry points
    entry_points={
        "console_scripts": [
            "python-service=app:create_app",
        ],
    },

    # Package classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],

    # Additional metadata
    keywords="flask microservice demo github-actions",
    project_urls={
        "Bug Reports": "https://github.com/example/github-actions-demo/issues",
        "Source": "https://github.com/example/github-actions-demo",
        "Documentation": "https://github.com/example/github-actions-demo#readme",
    },
)
