# Security Best Practices

This document outlines security considerations and best practices for GitHub Actions workflows.

## Overview

GitHub Actions is a powerful CI/CD platform, but with great power comes great responsibility. This guide covers security best practices to protect your workflows, secrets, and supply chain.

## Secret Management

### Types of Secrets

| Level | Scope | Use Case |
|-------|-------|----------|
| Repository | Single repo | Repo-specific credentials |
| Environment | Per environment | Deploy credentials |
| Organization | All repos | Shared credentials |

### Best Practices

#### 1. Never Hard-Code Secrets

```yaml
# ❌ BAD
- run: |
    API_KEY="sk_live_abcd1234"

# ✅ GOOD
- run: |
    echo "Using API key from secrets"
  env:
    API_KEY: ${{ secrets.API_KEY }}
```

#### 2. Use Environment-Specific Secrets

```yaml
deploy:
  environment: production
  steps:
    - run: deploy
      env:
        # Automatically uses production environment secret
        API_KEY: ${{ secrets.API_KEY }}
```

#### 3. Minimize Secret Scope

```yaml
permissions:
  contents: read  # Minimum required

# Only pass secrets to steps that need them
- name: Build
  run: npm run build
  
- name: Deploy
  run: deploy.sh
  env:
    DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}  # Only here
```

#### 4. Rotate Secrets Regularly

- Automate secret rotation where possible
- Document rotation procedures
- Use short-lived tokens when available

## Third-Party Actions

### Supply Chain Risks

Third-party actions can:
- Access repository secrets
- Execute arbitrary code
- Modify your codebase
- Exfiltrate data

### Mitigation Strategies

#### 1. Pin to SHA (Recommended)

```yaml
# ❌ Mutable tag - can be changed
uses: actions/checkout@v4

# ✅ Immutable SHA
uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
```

#### 2. Use Allowlists

Configure in **Settings** → **Actions** → **General**:

```
Allow select actions and reusable workflows:
  actions/*
  github/codeql-action/*
```

#### 3. Audit Before Use

Before adding a new action:
1. Review the source code
2. Check maintainer reputation
3. Review issue tracker
4. Look for security advisories

#### 4. Use Dependabot for Updates

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Workflow Permissions

### Least Privilege Principle

```yaml
# Global permissions (restrictive default)
permissions:
  contents: read

jobs:
  build:
    permissions:
      contents: read
      
  deploy:
    permissions:
      contents: read
      deployments: write  # Only where needed
```

### Available Permissions

| Permission | Use Case |
|------------|----------|
| `contents: read` | Checkout code |
| `contents: write` | Push commits |
| `pull-requests: write` | Comment on PRs |
| `issues: write` | Create/modify issues |
| `security-events: write` | Upload SARIF |
| `packages: write` | Publish packages |
| `deployments: write` | Create deployments |

### Fork PR Restrictions

Pull requests from forks have limited permissions:
- Cannot access secrets
- Read-only `GITHUB_TOKEN`
- Cannot trigger `pull_request_target` safely

## Branch Protection

### Recommended Settings

```
Branch: main
☑ Require pull request before merging
  ☑ Require approvals: 2
  ☑ Dismiss stale reviews
  ☑ Require review from code owners
☑ Require status checks to pass
  ☑ Require branches to be up to date
  - ci / build
  - security / scan
☑ Require signed commits
☑ Do not allow bypassing the above settings
```

### Status Check Requirements

Configure required workflows as status checks:

```yaml
# In branch protection rules
Required status checks:
  - ci / lint
  - ci / test
  - security / scan
```

## OIDC Authentication

### Why Use OIDC?

- No long-lived credentials
- Automatic token rotation
- Fine-grained permissions
- Audit trail

### AWS Example

```yaml
permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActions
          aws-region: us-east-1
```

### Azure Example

```yaml
- uses: azure/login@v1
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

## Code Scanning

### CodeQL Setup

```yaml
- uses: github/codeql-action/init@v3
  with:
    languages: python
    
- uses: github/codeql-action/analyze@v3
```

### Dependency Scanning

```yaml
- name: Python Dependencies
  run: pip-audit -r requirements.txt
  
- name: Node Dependencies
  run: npm audit --audit-level=high
```

## Artifact Security

### Sign Artifacts

```yaml
- name: Sign artifact
  run: |
    sha256sum dist/* > checksums.sha256
    gpg --sign checksums.sha256
```

### Verify Before Use

```yaml
- name: Verify checksum
  run: sha256sum -c checksums.sha256
```

### SLSA Provenance

```yaml
- uses: slsa-framework/slsa-github-generator/.github/workflows/builder_go_slsa3.yml@v1
```

## Security Checklist

### Repository Setup

- [ ] Enable Dependabot alerts
- [ ] Enable code scanning
- [ ] Enable secret scanning
- [ ] Configure branch protection
- [ ] Set up CODEOWNERS

### Workflow Security

- [ ] Pin all actions to SHA
- [ ] Minimize permissions
- [ ] Use environment secrets
- [ ] Enable OIDC for cloud auth
- [ ] Audit third-party actions

### Secret Hygiene

- [ ] No hardcoded secrets
- [ ] Regular rotation schedule
- [ ] Minimum necessary scope
- [ ] Documented procedures

### Ongoing Maintenance

- [ ] Weekly Dependabot reviews
- [ ] Monthly action audits
- [ ] Quarterly permission reviews
- [ ] Annual security assessment

## Incident Response

### If a Secret is Exposed

1. **Immediately rotate** the compromised secret
2. **Audit** recent workflow runs
3. **Check** for unauthorized access
4. **Update** all dependent systems
5. **Document** the incident

### If a Workflow is Compromised

1. **Disable** the workflow immediately
2. **Audit** recent runs for malicious activity
3. **Review** all changes to workflow files
4. **Check** artifact integrity
5. **Notify** affected teams

## Resources

- [GitHub Security Hardening Guide](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [SLSA Framework](https://slsa.dev/)
- [OpenSSF Scorecard](https://securityscorecards.dev/)
- [GitHub Advisory Database](https://github.com/advisories)
