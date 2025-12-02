# Setup Guide

This document provides instructions for setting up and running the GitHub Actions demonstration repository.

## Prerequisites

### Local Development

- Python 3.11 or higher
- pip (Python package manager)
- Git

### GitHub Actions

- GitHub repository with Actions enabled
- Appropriate permissions to configure workflows
- (Optional) Organization-level access for required workflows

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/github-actions-demo.git
cd github-actions-demo
```

### 2. Python Service Setup

```bash
cd apps/python-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Application

```bash
# Development mode
flask --app app run --debug

# Production mode (with Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### 4. Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
```

### 5. Running Linters

```bash
# Flake8
flake8 app tests

# Pylint
pylint app
```

## GitHub Configuration

### Repository Secrets

Configure these secrets in **Settings** → **Secrets and variables** → **Actions**:

| Secret | Description | Required |
|--------|-------------|----------|
| `PYPI_TOKEN` | PyPI publishing token | For releases |
| `SONAR_TOKEN` | SonarCloud integration | Optional |
| `SLACK_WEBHOOK` | Notification webhook | Optional |

### Repository Variables

Configure these variables in **Settings** → **Secrets and variables** → **Actions** → **Variables**:

| Variable | Default | Description |
|----------|---------|-------------|
| `DEFAULT_PYTHON_VERSION` | `3.11` | Python version for workflows |
| `BUILD_TIMEOUT_MINUTES` | `30` | Maximum build time |
| `TEST_PARALLELISM` | `4` | Parallel test workers |
| `ARTIFACT_RETENTION_DAYS` | `30` | Artifact retention period |

### Environment Setup

Create three environments in **Settings** → **Environments**:

#### Development Environment

1. Name: `development`
2. No protection rules (auto-deploy)
3. Secrets:
   - `DEV_API_ENDPOINT`: `https://dev-api.example.com`
4. Variables:
   - `ENVIRONMENT_NAME`: `development`
   - `LOG_LEVEL`: `debug`

#### Staging Environment

1. Name: `staging`
2. Protection rules:
   - Required reviewers: 1
   - Wait timer: 5 minutes
   - Deployment branches: `main`, `release/*`
3. Secrets:
   - `STAGING_API_ENDPOINT`: `https://staging-api.example.com`
4. Variables:
   - `ENVIRONMENT_NAME`: `staging`
   - `LOG_LEVEL`: `info`

#### Production Environment

1. Name: `production`
2. Protection rules:
   - Required reviewers: 2
   - Deployment branches: `main` only
   - Prevent self-review
3. Secrets:
   - `PROD_API_ENDPOINT`: `https://api.example.com`
   - `PROD_SIGNING_KEY`: (your signing key)
4. Variables:
   - `ENVIRONMENT_NAME`: `production`
   - `LOG_LEVEL`: `warn`

## Testing Workflows Locally

### Using act (nektos/act)

[act](https://github.com/nektos/act) allows you to run GitHub Actions locally.

#### Installation

```bash
# Mac
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows (with scoop)
scoop install act
```

#### Running Workflows

```bash
# List available workflows
act -l

# Run a specific workflow
act -W .github/workflows/ci.yml

# Run with specific event
act push

# Run with secrets
act -s GITHUB_TOKEN=your_token
```

#### Limitations

- Some GitHub features not available locally
- Self-hosted runner behaviors may differ
- Limited access to GitHub API

### Using Workflow Linting

#### actionlint

[actionlint](https://github.com/rhysd/actionlint) validates workflow syntax.

```bash
# Install
brew install actionlint  # Mac
go install github.com/rhysd/actionlint/cmd/actionlint@latest

# Run
actionlint
```

#### yamllint

For YAML validation:

```bash
pip install yamllint
yamllint .github/workflows/
```

## Troubleshooting

### Common Issues

#### 1. Workflow Not Triggering

**Symptoms**: Push/PR doesn't trigger workflow

**Solutions**:
- Check `on` trigger configuration
- Verify path filters match changed files
- Ensure branch is not excluded
- Check Actions are enabled for repository

#### 2. Permission Denied Errors

**Symptoms**: `Error: Resource not accessible by integration`

**Solutions**:
- Check `permissions` block in workflow
- Verify token has required scopes
- For forks, some permissions are restricted

#### 3. Cache Not Working

**Symptoms**: Dependencies re-downloaded every run

**Solutions**:
- Verify cache key includes dependency files
- Check cache is not full (10GB limit)
- Ensure restore-keys are correct

#### 4. Secrets Not Available

**Symptoms**: Secret is empty or undefined

**Solutions**:
- Verify secret name matches exactly (case-sensitive)
- Check environment is specified for environment secrets
- Forked PRs cannot access secrets

### Debug Mode

Enable debug logging by setting these secrets:

```
ACTIONS_RUNNER_DEBUG: true
ACTIONS_STEP_DEBUG: true
```

Or re-run with debug logging enabled in the UI.

### Getting Help

1. Check [GitHub Actions Documentation](https://docs.github.com/en/actions)
2. Search [GitHub Community Discussions](https://github.com/orgs/community/discussions)
3. Open an issue in this repository

## Next Steps

- Review [WORKFLOWS.md](./WORKFLOWS.md) for detailed workflow documentation
- Review [SECURITY.md](./SECURITY.md) for security best practices
- Review [ARCHITECTURE.md](./ARCHITECTURE.md) for design decisions
