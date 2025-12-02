# Architecture Documentation

This document explains the architectural decisions and patterns used in this GitHub Actions demonstration repository.

## Overview

This repository demonstrates enterprise-grade CI/CD patterns using GitHub Actions. It showcases various workflow organization strategies, reusable components, and best practices.

## Architectural Decision Records (ADRs)

### ADR-001: Stack-Specific Workflow Pattern

**Context**: We need to decide how to organize workflows for our Python application.

**Decision**: Use stack-specific workflows rather than a monolithic multi-stack workflow.

**Rationale**:
- Simpler to understand and maintain
- Independent release cycles
- Clear ownership per technology
- Easier troubleshooting

**Consequences**:
- Each stack has its own CI workflow
- Shared logic extracted to reusable workflows
- Slight duplication acceptable for clarity

### ADR-002: Reusable Workflows vs Composite Actions

**Context**: Need to share common logic across workflows.

**Decision**: Use both, based on use case:
- **Reusable Workflows**: Complete jobs with their own runners
- **Composite Actions**: Steps that run within a job

**Selection Criteria**:

| Criteria | Reusable Workflow | Composite Action |
|----------|-------------------|------------------|
| Needs own runner | ✅ | ❌ |
| Can have secrets | ✅ | Via inputs |
| Separate job in UI | ✅ | ❌ |
| Share outputs easily | ❌ | ✅ |
| Part of larger job | ❌ | ✅ |

### ADR-003: Environment Protection Strategy

**Context**: Need progressive deployment with appropriate gates.

**Decision**: Three-tier environment structure:

```
development → staging → production
     ↓            ↓           ↓
 No gates    1 reviewer   2 reviewers
             5 min wait   main only
```

**Rationale**:
- Development: Fast iteration
- Staging: Validation checkpoint
- Production: Maximum protection

### ADR-004: Action Version Pinning

**Context**: Balance between security and maintenance burden.

**Decision**: 
- Use SHA pinning for third-party actions
- Use major version tags for official GitHub actions
- Configure Dependabot for automated updates

**Example**:
```yaml
# Official GitHub action - major version OK
uses: actions/checkout@v4

# Third-party action - SHA required
uses: softprops/action-gh-release@de2c0eb89ae2a093876385947365aca7b0e5f844
```

## Component Architecture

### Workflow Hierarchy

```
┌─────────────────────────────────────────────────────┐
│                 Trigger Events                       │
│     (push, pull_request, schedule, dispatch)        │
└──────────────────────┬──────────────────────────────┘
                       │
           ┌───────────▼───────────┐
           │   Main Workflows      │
           │   (ci.yml, etc.)      │
           └───────────┬───────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌───────────┐  ┌───────────┐  ┌───────────┐
│ Reusable  │  │ Reusable  │  │ Reusable  │
│ Workflows │  │ Workflows │  │ Workflows │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
           ┌─────────▼─────────┐
           │ Composite Actions │
           └─────────┬─────────┘
                     │
           ┌─────────▼─────────┐
           │  Official GitHub  │
           │     Actions       │
           └───────────────────┘
```

### Directory Structure

```
.github/
├── workflows/                    # Workflow definitions
│   ├── ci.yml                   # Main CI pipeline
│   ├── pr-validation.yml        # PR checks
│   ├── release.yml              # Release process
│   ├── environment-demo.yml     # Environment demo
│   ├── required-security.yml    # Security baseline
│   ├── required-compliance.yml  # Compliance checks
│   ├── dependency-update.yml    # Dependency automation
│   ├── performance-benchmark.yml # Performance tests
│   ├── marketplace-policy-demo.yml
│   └── reusable/                # Reusable workflows
│       ├── security-scan.yml
│       ├── build-test.yml
│       └── release-validation.yml
├── actions/                      # Composite actions
│   ├── setup-build-env/
│   ├── quality-checks/
│   └── package-artifacts/
└── COPILOT_PROMPT.md            # Project requirements
```

## Caching Strategy

### Cache Hierarchy

```
┌─────────────────────────────────────┐
│          GitHub Cache              │
│         (10GB per repo)            │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────┐  ┌─────────────┐  │
│  │   Python    │  │    Node     │  │
│  │ pip cache   │  │  npm cache  │  │
│  └─────────────┘  └─────────────┘  │
│                                     │
│  Cache Keys:                        │
│  • OS-language-hash(lockfile)      │
│  • Restore keys for partial match  │
│                                     │
└─────────────────────────────────────┘
```

### Cache Key Strategy

```yaml
# Python caching
key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
restore-keys: |
  ${{ runner.os }}-pip-

# Node.js caching  
key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
restore-keys: |
  ${{ runner.os }}-node-
```

### Cache Invalidation

Caches are invalidated when:
1. Key hash changes (dependency updates)
2. 7 days have passed (GitHub limit)
3. Cache size exceeds 10GB (LRU eviction)

## Artifact Lifecycle

```
┌──────────────────────────────────────────────────────┐
│                    Build Job                          │
│                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Build     │──│  Package    │──│   Upload    │  │
│  │   Output    │  │  Artifacts  │  │  to GitHub  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│              Artifact Storage                         │
│                                                       │
│  Retention: 30 days (configurable)                   │
│  Max size: 500MB per artifact                        │
│  Format: ZIP compression                              │
│                                                       │
└──────────────────────────┬───────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │  Release  │   │   Test    │   │  Deploy   │
    │  Asset    │   │  Report   │   │  Package  │
    └───────────┘   └───────────┘   └───────────┘
```

## Security Architecture

### Permission Model

```
┌─────────────────────────────────────────────────────┐
│              Workflow Permissions                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Global Default: contents: read (restrictive)       │
│                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Lint      │  │   Test      │  │   Deploy    │ │
│  │ read only   │  │ read + PR   │  │ read + dep  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Secret Scope

```
Organization Secrets
      │
      ├── ORG_DOCKER_REGISTRY
      └── ORG_SECURITY_SCANNER_KEY
      
Repository Secrets
      │
      ├── PYPI_TOKEN
      ├── SONAR_TOKEN
      └── SLACK_WEBHOOK
      
Environment Secrets
      │
      ├── development/
      │     └── DEV_API_ENDPOINT
      ├── staging/
      │     └── STAGING_API_ENDPOINT
      └── production/
            ├── PROD_API_ENDPOINT
            └── PROD_SIGNING_KEY
```

## Scaling Considerations

### Matrix Builds

```yaml
strategy:
  matrix:
    python: ['3.11', '3.12']
    os: [ubuntu-latest, macos-latest]
```

Creates 4 parallel jobs (2 versions × 2 OS).

### Concurrency Control

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Prevents resource waste from obsolete runs.

### Self-Hosted Runners

For high-volume repos, consider self-hosted runners:
- Faster builds (persistent cache)
- Custom hardware/software
- Cost control for heavy usage

## Monitoring and Observability

### Job Summaries

```yaml
- run: |
    echo "## Build Results" >> $GITHUB_STEP_SUMMARY
    echo "| Metric | Value |" >> $GITHUB_STEP_SUMMARY
    echo "|--------|-------|" >> $GITHUB_STEP_SUMMARY
    echo "| Duration | ${{ steps.build.duration }} |" >> $GITHUB_STEP_SUMMARY
```

### Annotations

```yaml
- run: |
    echo "::error file=app.py,line=10::Syntax error"
    echo "::warning::Deprecated function used"
```

### Debug Logging

```yaml
env:
  ACTIONS_RUNNER_DEBUG: true
  ACTIONS_STEP_DEBUG: true
```

## Future Improvements

### Planned Enhancements

1. **Container Builds**: Add Docker image building and pushing
2. **Deployment Automation**: Kubernetes/cloud deployments
3. **Feature Flags**: Environment-based feature toggles
4. **Metrics Collection**: Build time and success rate tracking

### Migration Path

Current → Future:
- Single region → Multi-region deployment
- Manual releases → Continuous deployment
- Basic security → SLSA Level 3 compliance
