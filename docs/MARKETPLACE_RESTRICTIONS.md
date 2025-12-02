# GitHub Actions Marketplace Restrictions

This document explains how to configure and manage GitHub Actions marketplace restrictions to secure your CI/CD pipelines against supply chain attacks.

## Overview

GitHub Actions marketplace contains thousands of actions created by the community. While this provides great flexibility, it also introduces security risks. Marketplace restrictions allow you to control which actions can run in your repositories.

## Security Risks of Third-Party Actions

### Supply Chain Attacks

Third-party actions can:
- Access all repository secrets
- Execute arbitrary code in your environment
- Exfiltrate sensitive data
- Modify your codebase
- Deploy malicious code to production

### Common Attack Vectors

1. **Compromised Maintainer Account**: Attacker gains access to action maintainer's account
2. **Dependency Confusion**: Malicious packages with similar names
3. **Tag Mutable References**: Attacker modifies tagged release
4. **Hidden Malicious Code**: Obfuscated code in action

## Policy Tiers

### 1. Allow All Actions ❌ Not Recommended

**Configuration**: Allow any action from the marketplace

```
Settings > Actions > General
Action permissions: Allow all actions and reusable workflows
```

**Risk Profile**: 🔴 HIGH

**Use Cases**:
- Proof of concept only
- Personal learning projects
- Completely sandboxed environments

**Why to Avoid**:
- No control over what runs
- Maximum attack surface
- No audit trail of allowed actions

### 2. Allow Verified Creators Only ⚠️

**Configuration**: Only actions from GitHub-verified creators

```
Settings > Actions > General
Action permissions: Allow GitHub Actions, and actions from verified creators
```

**Risk Profile**: 🟡 MEDIUM

**Verified Creators Include**:
- GitHub (`actions/*`)
- Microsoft
- Docker
- AWS, Google, Azure
- Other major vendors

**Benefits**:
- Reduced attack surface
- Reputable maintainers
- Regular security updates

**Limitations**:
- May block useful community actions
- Verification ≠ security guarantee
- Still allows many actions

### 3. Allow Specific Actions ✅ Recommended

**Configuration**: Only explicitly allowed actions can run

```
Settings > Actions > General
Action permissions: Allow select actions and reusable workflows
```

**Risk Profile**: 🟢 LOW

**Example Allowlist**:

```
# Official GitHub Actions
actions/checkout@*
actions/setup-node@*
actions/setup-python@*
actions/setup-java@*
actions/setup-dotnet@*
actions/cache@*
actions/upload-artifact@*
actions/download-artifact@*

# GitHub Security
github/codeql-action/*

# Trusted Third-Party
docker/build-push-action@*
softprops/action-gh-release@*
codecov/codecov-action@*

# Cloud Providers
aws-actions/configure-aws-credentials@*
azure/webapps-deploy@*
google-github-actions/auth@*
```

**Best Practices**:
1. Start with minimal set
2. Add actions as needed
3. Review before adding
4. Audit regularly
5. Pin to SHA for immutability

### 4. Allow Local Actions Only 🔒

**Configuration**: Only actions within repository/organization

```
Settings > Actions > General
Action permissions: Allow local actions only
```

**Risk Profile**: 🟢 LOWEST

**Use Cases**:
- Air-gapped environments
- Highly regulated industries
- Maximum security posture
- Government/defense contractors

**Requirements**:
- Create composite actions for all needs
- Maintain all action code internally
- Higher development overhead

## Implementing Action Allowlists

### Repository Level

1. Go to **Settings** → **Actions** → **General**
2. Under **Actions permissions**, select **Allow select actions**
3. Add allowed patterns in the text box

### Organization Level

1. Go to **Organization Settings** → **Actions** → **General**
2. Configure default policy for all repositories
3. Patterns apply to entire organization

### Allowlist Patterns

```
# Exact match
actions/checkout@v4

# Any version of specific action
actions/checkout@*

# Any action from organization
actions/*

# Specific SHA (most secure)
actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

# Wildcard for sub-actions
github/codeql-action/*
```

## Version Pinning Strategies

### Strategy 1: Major Version Tags ⚠️

```yaml
uses: actions/checkout@v4
```

**Pros**: Gets security updates automatically
**Cons**: Breaking changes possible

### Strategy 2: Full Version Tags

```yaml
uses: actions/checkout@v4.1.1
```

**Pros**: More predictable
**Cons**: May miss security patches

### Strategy 3: SHA Pinning ✅ Recommended

```yaml
uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
```

**Pros**: Immutable, maximum security
**Cons**: Manual updates required

### Automating SHA Updates

Use Dependabot or Renovate:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "chore(deps)"
```

## Local Actions as Alternatives

### Creating Composite Actions

Replace third-party actions with local composites:

```yaml
# .github/actions/setup-environment/action.yml
name: 'Setup Environment'
description: 'Local replacement for third-party setup actions'

inputs:
  language:
    description: 'Programming language'
    required: true

runs:
  using: 'composite'
  steps:
    - name: Setup Python
      if: inputs.language == 'python'
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
```

### Benefits of Local Actions

1. **Full Control**: You own and review all code
2. **Customization**: Tailored to your needs
3. **No External Dependencies**: Works in air-gapped environments
4. **Consistent Behavior**: No surprise updates

## Auditing and Compliance

### Regular Audits

1. Review all actions in use
2. Check for new vulnerabilities
3. Verify SHA pins are current
4. Remove unused actions

### Audit Script

```bash
#!/bin/bash
# Find all actions used in workflows
grep -rh "uses:" .github/workflows/*.yml | \
  grep -v "uses: ./" | \
  sort | uniq -c | sort -rn
```

### Compliance Checklist

- [ ] All actions pinned to SHA
- [ ] No actions from unverified creators
- [ ] Security review for each action
- [ ] Quarterly allowlist review
- [ ] Dependabot configured for updates

## Terraform Configuration

Manage restrictions via infrastructure as code:

```hcl
resource "github_actions_organization_permissions" "this" {
  allowed_actions      = "selected"
  enabled_repositories = "all"

  allowed_actions_config {
    github_owned_allowed = true
    verified_allowed     = false
    patterns_allowed     = [
      "actions/*",
      "github/codeql-action/*",
      "docker/build-push-action@*"
    ]
  }
}
```

## Migration Guide

### From "Allow All" to "Specific Actions"

1. **Audit Current Usage**
   ```bash
   grep -rh "uses:" .github/workflows/ | sort | uniq
   ```

2. **Create Initial Allowlist**
   Start with actions currently in use

3. **Test in Non-Production**
   Enable on test repositories first

4. **Enable Evaluate Mode**
   See what would be blocked without blocking

5. **Activate Restrictions**
   Enable for production after testing

6. **Monitor and Adjust**
   Add legitimate actions as needed

## Related Resources

- [GitHub Docs: Managing Actions Permissions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
- [GitHub Security Hardening Guide](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [SLSA Framework](https://slsa.dev/)
