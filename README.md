# GitHub Actions Comprehensive Demo

[![CI](https://github.com/mastercard-actions-demo/python-app/actions/workflows/ci.yml/badge.svg)](https://github.com/mastercard-actions-demo/python-app/actions/workflows/ci.yml)
[![Security Scan](https://github.com/mastercard-actions-demo/python-app/actions/workflows/required-security.yml/badge.svg)](https://github.com/mastercard-actions-demo/python-app/actions/workflows/required-security.yml)

A comprehensive GitHub Actions demonstration repository showcasing enterprise-grade CI/CD patterns, security best practices, and advanced workflow features.

## 🎯 Purpose

This repository serves as an educational and reference implementation for:

- Enterprise CI/CD pipeline patterns
- GitHub Actions best practices
- Security and compliance workflows
- Reusable workflow components
- Environment-based deployments

## 📁 Repository Structure

```
├── apps/
│   └── python-service/          # Python Flask microservice
├── docs/
│   ├── SETUP.md                 # Setup instructions
│   ├── WORKFLOWS.md             # Workflow documentation
│   ├── SECURITY.md              # Security best practices
│   ├── ARCHITECTURE.md          # Architecture decisions
│   ├── REQUIRED_WORKFLOWS.md    # Required workflow setup
│   └── MARKETPLACE_RESTRICTIONS.md  # Action policies
├── .github/
│   ├── app-ci.json             # Central required CI project and extension config
│   ├── ci/                     # Optional app-specific CI extensions
│   ├── workflows/               # Workflow definitions
│   │   ├── ci.yml              # Main CI pipeline
│   │   ├── pr-validation.yml   # PR checks
│   │   ├── release.yml         # Release process
│   │   ├── environment-demo.yml
│   │   ├── required-security.yml
│   │   ├── required-compliance.yml
│   │   ├── dependency-update.yml
│   │   ├── performance-benchmark.yml
│   │   ├── marketplace-policy-demo.yml
│   │   └── reusable/           # Reusable workflows
│   │       ├── security-scan.yml
│   │       ├── build-test.yml
│   │       └── release-validation.yml
│   └── actions/                 # Composite actions
│       ├── setup-build-env/
│       ├── quality-checks/
│       └── package-artifacts/
└── README.md
```

## 🚀 Quick Start

### Python Service

```bash
cd apps/python-service

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
flask --app app run --debug

# Run tests
pytest --cov=app --cov-report=term-missing
```

## 🔧 Features Demonstrated

### Workflow Patterns

| Pattern | File | Description |
|---------|------|-------------|
| Stack-Specific CI | `ci.yml` | Dedicated workflow for Python stack |
| PR Validation | `pr-validation.yml` | Comprehensive PR checks |
| Release Automation | `release.yml` | Tag-triggered releases |
| Environment Deploy | `environment-demo.yml` | Protected deployments |
| Local Security Demo | `required-security.yml` | Repository-local security workflow example |
| Local Compliance Demo | `required-compliance.yml` | Repository-local compliance workflow example |

### Organization-Required CI

The organization-required workflow is maintained centrally in
[`gclhub-actions-demo/required-workflows`](https://github.com/gclhub-actions-demo/required-workflows).
It is enforced by an organization ruleset for pull requests targeting `main`; it is
separate from this repository's local workflows and also runs for documentation-only
changes. The central policy requires Python 3.11, flake8, pytest with an 80% minimum
coverage threshold, and a package build.

The central workflow discovers this application's project through
[`.github/app-ci.json`](.github/app-ci.json). Its optional preflight and postflight
scripts are app-specific additions, not replacements for the required checks. They
run independently in fresh hosted jobs, so they must not depend on files or artifacts
produced by the other jobs. The scripts validate the Python service layout and
declared package metadata; they do not require secrets or write permissions.

The existing `required-security.yml` and `required-compliance.yml` files remain
repository-local demonstration workflows; their names do not make them the
organization-required gate.

### Reusable Components

**Reusable Workflows** (`.github/workflows/reusable/`):
- `security-scan.yml` - Centralized security scanning
- `build-test.yml` - Generic build and test pattern
- `release-validation.yml` - Pre-release validation

**Composite Actions** (`.github/actions/`):
- `setup-build-env` - Multi-stack environment setup
- `quality-checks` - Unified code quality validation
- `package-artifacts` - Standardized artifact packaging

### Advanced Features

- ✅ Matrix builds (Python 3.11, 3.12)
- ✅ Dependency caching
- ✅ Concurrency control
- ✅ Environment protection rules
- ✅ Workflow dispatch with inputs
- ✅ Job summaries and annotations
- ✅ Artifact upload/download
- ✅ Scheduled workflows

## 🔒 Security Features

- **Secret scanning simulation**
- **Dependency vulnerability scanning**
- **SAST with Bandit**
- **License compliance checks**
- **Commit signature verification**
- **Branch protection integration**
- **OIDC authentication examples**

See [docs/SECURITY.md](docs/SECURITY.md) for detailed security documentation.

## 🌍 Environments

| Environment | Protection | Use Case |
|-------------|------------|----------|
| `development` | None | Auto-deploy on push |
| `staging` | 1 reviewer, 5 min wait | Gated deployment |
| `production` | 2 reviewers, main only | Production deploy |

## 📖 Documentation

- [Setup Guide](docs/SETUP.md) - Getting started
- [Workflows](docs/WORKFLOWS.md) - Detailed workflow documentation
- [Security](docs/SECURITY.md) - Security best practices
- [Architecture](docs/ARCHITECTURE.md) - Design decisions
- [Required Workflows](docs/REQUIRED_WORKFLOWS.md) - Org-level enforcement
- [Marketplace Restrictions](docs/MARKETPLACE_RESTRICTIONS.md) - Action policies

## 🏗️ Configuration

### Repository Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEFAULT_PYTHON_VERSION` | `3.11` | Python version |
| `BUILD_TIMEOUT_MINUTES` | `30` | Max build time |
| `ARTIFACT_RETENTION_DAYS` | `30` | Artifact retention |

### Required Secrets

| Secret | Purpose |
|--------|---------|
| `PYPI_TOKEN` | PyPI publishing |
| `SONAR_TOKEN` | SonarCloud integration |
| `SLACK_WEBHOOK` | Notifications |

## 🧪 Testing Locally

### Using act

```bash
# Install act
brew install act  # macOS

# Run CI workflow locally
act -W .github/workflows/ci.yml
```

### Workflow Linting

```bash
# Install actionlint
brew install actionlint

# Lint all workflows
actionlint
```

## 📚 GitHub Documentation References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Reusing Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Creating Composite Actions](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
- [Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Managing Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
