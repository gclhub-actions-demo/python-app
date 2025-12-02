# Workflows Documentation

This document provides detailed documentation for all workflows in this repository.

## Workflow Overview

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | Push, PR | Main CI pipeline for Python service |
| `pr-validation.yml` | PR | Comprehensive PR checks |
| `release.yml` | Tag push | Release and artifact publishing |
| `environment-demo.yml` | Manual, Push | Environment deployment demo |
| `required-security.yml` | Push, PR | Security baseline checks |
| `required-compliance.yml` | Push, PR | Compliance verification |
| `dependency-update.yml` | Schedule | Dependency update automation |
| `performance-benchmark.yml` | Schedule | Performance testing |
| `marketplace-policy-demo.yml` | Manual | Action restriction demos |

## Main CI Workflow (`ci.yml`)

### Purpose

The primary CI workflow for the Python microservice, demonstrating enterprise-grade CI/CD patterns.

### Triggers

```yaml
on:
  push:
    branches: [main, develop]
    paths: ['apps/python-service/**']
  pull_request:
    branches: [main, develop]
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'
```

### Jobs

1. **lint**: Code quality checks with flake8 and pylint
2. **test**: Unit tests with coverage (matrix: Python 3.11, 3.12)
3. **security-scan**: Bandit security analysis
4. **build**: Package creation for releases
5. **summary**: Pipeline status aggregation

### Key Features

- Matrix builds for Python versions
- Dependency caching
- Coverage reporting
- Artifact upload
- Concurrency control

### Usage

```yaml
# Runs automatically on push/PR
# Manual trigger:
gh workflow run ci.yml
```

## PR Validation (`pr-validation.yml`)

### Purpose

Comprehensive pull request validation including size analysis, labeling, and quality checks.

### Features

- PR size analysis (XS, S, M, L, XL)
- Change type detection
- Automated PR comments
- Quality gate enforcement

### Outputs

| Output | Description |
|--------|-------------|
| `size` | PR size category |
| `files-changed` | Number of files changed |
| `lines-changed` | Total lines changed |

## Release Workflow (`release.yml`)

### Purpose

Handles the complete release process from tag creation to artifact publishing.

### Triggers

```yaml
on:
  push:
    tags:
      - 'v[0-9]+.[0-9]+.[0-9]+*'
  workflow_dispatch:
    inputs:
      tag: { required: true }
      deploy_to_staging: { default: false }
```

### Process

1. Validate semantic version
2. Build all applications
3. Run full test suite
4. Create GitHub Release
5. Generate changelog
6. (Optional) Deploy to staging

### Creating a Release

```bash
# Create and push tag
git tag v1.0.0
git push origin v1.0.0
```

## Environment Demo (`environment-demo.yml`)

### Purpose

Demonstrates GitHub environments with protection rules.

### Environments

| Environment | Protection | Use Case |
|-------------|------------|----------|
| `development` | None | Auto-deploy |
| `staging` | 1 reviewer, 5 min wait | Gated deployment |
| `production` | 2 reviewers, main only | Production deploy |

### Usage

```bash
# Manual trigger with environment selection
gh workflow run environment-demo.yml \
  -f environment=staging \
  -f deploy_version=v1.0.0
```

## Reusable Workflows

### Security Scan (`reusable/security-scan.yml`)

**Inputs**:
| Input | Type | Description |
|-------|------|-------------|
| `language` | string | Programming language |
| `scan-type` | string | sast, sca, secrets, all |
| `severity-threshold` | string | critical, high, medium, low |

**Outputs**:
| Output | Description |
|--------|-------------|
| `vulnerabilities-found` | Boolean |
| `critical-count` | Number of criticals |
| `scan-status` | success/warning/failure |

**Usage**:
```yaml
jobs:
  security:
    uses: ./.github/workflows/reusable/security-scan.yml
    with:
      language: python
      scan-type: all
      severity-threshold: high
```

### Build and Test (`reusable/build-test.yml`)

**Inputs**:
| Input | Type | Description |
|-------|------|-------------|
| `working-directory` | string | Path to app |
| `stack-type` | string | python, node, java, dotnet |
| `upload-artifacts` | boolean | Upload build outputs |
| `test-command` | string | Custom test command |

**Outputs**:
| Output | Description |
|--------|-------------|
| `build-status` | success/failure |
| `test-coverage` | Coverage percentage |

### Release Validation (`reusable/release-validation.yml`)

**Inputs**:
| Input | Type | Description |
|-------|------|-------------|
| `version` | string | Semver version |
| `environment` | string | Target environment |
| `require-approval` | boolean | Manual approval needed |

**Outputs**:
| Output | Description |
|--------|-------------|
| `validation-status` | Overall status |
| `version-valid` | Semver validation result |

## Composite Actions

### Setup Build Environment (`.github/actions/setup-build-env`)

Sets up the build environment for any supported stack.

```yaml
- uses: ./.github/actions/setup-build-env
  with:
    stack-type: python
    stack-version: '3.11'
    enable-cache: true
```

### Quality Checks (`.github/actions/quality-checks`)

Runs linting and security scanning.

```yaml
- uses: ./.github/actions/quality-checks
  with:
    working-directory: apps/python-service
    linter: auto
    fail-on-error: true
```

### Package Artifacts (`.github/actions/package-artifacts`)

Packages and uploads build artifacts.

```yaml
- uses: ./.github/actions/package-artifacts
  with:
    artifact-name: my-app-v1.0.0
    working-directory: dist
    retention-days: 30
```

## Workflow Best Practices

### 1. Use Concurrency Control

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### 2. Minimize Permissions

```yaml
permissions:
  contents: read
  pull-requests: write
```

### 3. Cache Dependencies

```yaml
- uses: actions/setup-python@v5
  with:
    cache: 'pip'
```

### 4. Use Job Summaries

```yaml
- run: |
    echo "## Results" >> $GITHUB_STEP_SUMMARY
    echo "✅ All tests passed" >> $GITHUB_STEP_SUMMARY
```

### 5. Pin Action Versions

```yaml
# Prefer SHA pinning for security
uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
```

## Workflow Status Badges

Add these badges to your README:

```markdown
![CI](https://github.com/your-org/repo/actions/workflows/ci.yml/badge.svg)
![Security](https://github.com/your-org/repo/actions/workflows/required-security.yml/badge.svg)
```
