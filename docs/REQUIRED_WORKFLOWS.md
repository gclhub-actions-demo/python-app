# Required Workflows in Organization Rulesets

This document explains how to configure and use required workflows at the organization level to enforce consistent policies across all repositories.

## Overview

Required workflows are organization-level workflows that run on all or selected repositories when triggered by specific events (like pull requests). They cannot be bypassed or disabled at the repository level, making them ideal for enforcing security and compliance policies.

## Key Concepts

### What are Required Workflows?

- Workflows that must run and pass before code can be merged
- Configured at the organization level via rulesets
- Apply to multiple repositories based on patterns
- Cannot be disabled or modified by repository admins

### Benefits

1. **Consistent Security**: Ensure all repositories meet security standards
2. **Compliance Enforcement**: Mandate compliance checks across the organization
3. **Reduced Overhead**: Define once, apply everywhere
4. **Audit Trail**: Centralized logging of policy enforcement

## Setting Up Required Workflows

### Step 1: Create the Required Workflow

First, create a workflow file in a central repository (e.g., `.github-workflows` repository):

```yaml
# .github/workflows/required-security.yml
name: Required Security Baseline

on:
  workflow_call:  # Required for reusable workflows

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Security Scan
        run: |
          # Your security scanning logic
          echo "Running security checks..."
```

### Step 2: Create Organization Ruleset

1. Navigate to **Organization Settings** → **Code security and analysis** → **Rulesets**
2. Click **New ruleset** → **New branch ruleset**
3. Configure the ruleset:

```
Name: Security Requirements
Enforcement status: Active
Target repositories: All repositories (or specific patterns)
```

### Step 3: Add Required Workflow

1. In the ruleset, find **Require workflows to pass before merging**
2. Click **Add workflow**
3. Select the repository containing the required workflow
4. Choose the workflow file

### Step 4: Configure Branch Protection

```
Branches:
  - main
  - develop
  - release/*

Rules:
  - Require a pull request before merging
  - Require workflows to pass before merging
    - Workflow: org/repo/.github/workflows/required-security.yml@main
```

## Example Required Workflows

### 1. Security Baseline

**Purpose**: Ensure all code meets minimum security standards

```yaml
name: Required Security Baseline

on:
  workflow_call:

permissions:
  contents: read
  security-events: write

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check for Secrets
        run: |
          # Scan for accidentally committed secrets
          if grep -rE "AKIA[0-9A-Z]{16}" .; then
            echo "AWS key found!"
            exit 1
          fi

  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Scan Dependencies
        run: |
          # Check for vulnerable dependencies
          pip install pip-audit
          pip-audit || exit 1

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
      - uses: github/codeql-action/analyze@v3
```

### 2. Compliance and Audit

**Purpose**: Enforce organizational compliance policies

```yaml
name: Required Compliance Check

on:
  workflow_call:

jobs:
  verify-files:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check Required Files
        run: |
          MISSING=0
          for file in LICENSE README.md SECURITY.md; do
            if [ ! -f "$file" ]; then
              echo "Missing: $file"
              MISSING=$((MISSING + 1))
            fi
          done
          exit $MISSING

  branch-naming:
    runs-on: ubuntu-latest
    steps:
      - name: Validate Branch Name
        run: |
          BRANCH="${GITHUB_HEAD_REF}"
          if [[ ! "$BRANCH" =~ ^(feature|bugfix|hotfix|release)/ ]]; then
            echo "Invalid branch name: $BRANCH"
            exit 1
          fi
```

## Best Practices

### 1. Design for Minimal Impact

Required workflows run on every PR, so keep them:
- Fast (under 5 minutes)
- Focused on critical checks only
- Efficient with caching

### 2. Provide Clear Feedback

```yaml
- name: Security Check
  run: |
    if [ "$FAILED" = true ]; then
      echo "::error::Security check failed: $REASON"
      echo "See documentation at: https://docs.example.com/security"
      exit 1
    fi
```

### 3. Allow Graceful Degradation

```yaml
- name: Non-Critical Check
  continue-on-error: true
  run: |
    # This check warns but doesn't block
    echo "::warning::Consider improving test coverage"
```

### 4. Version Your Workflows

Reference specific versions in rulesets:

```
org/repo/.github/workflows/security.yml@v1.0.0
org/repo/.github/workflows/security.yml@main
```

### 5. Test Before Enforcing

Use "Evaluate" mode before "Active":

```
Enforcement status: Evaluate
```

This logs what would happen without actually blocking merges.

## Terraform Configuration

For infrastructure-as-code management of rulesets, use the GitHub Terraform provider:

```hcl
# Organization ruleset for required workflows
resource "github_organization_ruleset" "security_required" {
  name        = "Security Requirements"
  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = ["~DEFAULT_BRANCH", "refs/heads/release/*"]
      exclude = []
    }
  }

  rules {
    required_workflows {
      required_workflow {
        path           = ".github/workflows/required-security.yml"
        repository_id  = github_repository.workflows_repo.repo_id
        ref            = "refs/heads/main"
      }
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Workflow not triggering**
   - Check if `workflow_call` trigger is present
   - Verify ruleset is set to "Active"
   - Confirm repository matches target pattern

2. **Workflow failing unexpectedly**
   - Check workflow permissions
   - Verify secrets are available at org level
   - Review workflow run logs

3. **Performance issues**
   - Enable caching in workflows
   - Use matrix strategies carefully
   - Consider self-hosted runners

## Related Documentation

- [GitHub Docs: Managing Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [GitHub Docs: Reusing Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [GitHub Terraform Provider](https://registry.terraform.io/providers/integrations/github/latest/docs)
