# GitHub Actions Comprehensive Demo - Implementation Prompt

## Project Overview
Create a comprehensive GitHub Actions demonstration repository showcasing enterprise-grade CI/CD patterns, Python technology stack support, security best practices, and advanced workflow features.

## Repository Structure Requirements

### 1. Python Technology Stack Support

Create Python application technology stack to demonstrate versatile CI/CD patterns:

#### Technology Stack: Python
- **Location**: `apps/python-service/`
- **Purpose**: Python microservice with Flask
- **Features**:
  - Python 3.11+ compatibility
  - pylint/flake8 linting
  - pytest unit tests with coverage
  - pip dependency caching with requirements.txt
  - Build wheel distribution
  - Setup.py or pyproject.toml

### 2. Workflow Organization Strategies

Demonstrate architectural pattern:

#### Pattern B: Stack-Specific Workflow
- **Files**:
  - `.github/workflows/ci.yml`
- **Strategy**: Dedicated workflow per technology stack
- **Use Case**: Smaller teams, independent release cycles, specialized configurations
- **Features**:
  - Stack-specific optimizations
  - Independent status checks
  - Technology-specific tooling versions

### 3. Reusable Workflows

Create reusable workflows in `.github/workflows/reusable/`:

#### Reusable Workflow 1: Security Scanning
- **File**: `.github/workflows/reusable/security-scan.yml`
- **Purpose**: Centralized security scanning
- **Inputs**:
  - `language`: Programming language (python)
  - `scan-type`: Type of scan (sast, sca, secrets)
  - `severity-threshold`: Fail threshold (critical, high, medium, low)
- **Outputs**:
  - `vulnerabilities-found`: Boolean
  - `critical-count`: Number of critical issues
- **Features**:
  - CodeQL analysis
  - Dependency scanning
  - Secret scanning simulation
  - SARIF upload to GitHub Security tab

#### Reusable Workflow 2: Build and Test
- **File**: `.github/workflows/reusable/build-test.yml`
- **Purpose**: Generic build and test pattern
- **Inputs**:
  - `working-directory`: Path to app
  - `stack-type`: Technology stack identifier
  - `upload-artifacts`: Boolean for artifact upload
  - `artifact-name`: Name for build artifacts
  - `test-command`: Custom test command
- **Outputs**:
  - `build-status`: Success/failure
  - `test-coverage`: Coverage percentage
- **Features**:
  - Dynamic tool setup based on stack
  - Dependency caching
  - Test result publishing
  - Artifact upload with retention policies

#### Reusable Workflow 3: Release Validation
- **File**: `.github/workflows/reusable/release-validation.yml`
- **Purpose**: Pre-release checks and validation
- **Inputs**:
  - `version`: Release version
  - `environment`: Target environment (dev, staging, prod)
  - `require-approval`: Boolean for manual approval
- **Features**:
  - Semantic version validation
  - Changelog verification
  - Tag existence check
  - Environment-based validation rules

### 4. Composite Actions

Create custom composite actions in `.github/actions/`:

#### Composite Action 1: Setup Build Environment
- **Path**: `.github/actions/setup-build-env/action.yml`
- **Purpose**: Standardize environment setup across workflows
- **Inputs**:
  - `stack-type`: Technology stack (node, python, java, dotnet)
  - `stack-version`: Version to install
  - `enable-cache`: Boolean for dependency caching
  - `cache-key-prefix`: Custom cache key prefix
- **Steps**:
  - Detect and setup language runtime
  - Configure package manager
  - Setup dependency caching with automatic key generation
  - Install build tools
  - Print environment diagnostics

#### Composite Action 2: Run Quality Checks
- **Path**: `.github/actions/quality-checks/action.yml`
- **Purpose**: Unified code quality validation
- **Inputs**:
  - `working-directory`: Path to analyze
  - `linter`: Linter to use (auto-detect if not specified)
  - `fail-on-error`: Boolean to fail on quality issues
  - `upload-results`: Boolean to upload SARIF results
- **Steps**:
  - Run linter based on stack
  - Run security linter (Semgrep, Bandit, etc.)
  - Generate quality report
  - Comment PR with results (if in PR context)

#### Composite Action 3: Package and Publish Artifacts
- **Path**: `.github/actions/package-artifacts/action.yml`
- **Purpose**: Standardize artifact creation and upload
- **Inputs**:
  - `artifact-name`: Name for artifact
  - `working-directory`: Build output location
  - `retention-days`: Artifact retention period
  - `include-patterns`: Files to include (glob)
  - `exclude-patterns`: Files to exclude (glob)
- **Steps**:
  - Collect build outputs
  - Generate artifact manifest (SHA checksums, metadata)
  - Create compressed archive
  - Upload to GitHub Actions artifacts
  - Generate artifact download URL

### 5. Secrets, Variables, and Environments

#### GitHub Secrets Configuration (Document in README)
Create documentation for the following secrets:

**Repository Secrets**:
- `NPM_TOKEN`: npm registry authentication
- `PYPI_TOKEN`: PyPI publishing token
- `SONAR_TOKEN`: SonarCloud integration
- `SLACK_WEBHOOK`: Notification webhook

**Organization Secrets** (if applicable):
- `ORG_DOCKER_REGISTRY`: Container registry URL
- `ORG_SECURITY_SCANNER_KEY`: Security tool API key

#### GitHub Variables Configuration
Create examples using GitHub variables:

**Repository Variables**:
- `BUILD_TIMEOUT_MINUTES`: Maximum build time (default: 30)
- `TEST_PARALLELISM`: Number of parallel test workers (default: 4)
- `ARTIFACT_RETENTION_DAYS`: Default retention (default: 30)
- `ENABLE_SECURITY_SCAN`: Feature flag (default: true)
- `DEFAULT_PYTHON_VERSION`: Python version (default: 3.11)

**Environment-Specific Variables**:
- Per environment (development, staging, production)
- API endpoints, feature flags, resource limits

#### Environments with Protection Rules

Create three environments demonstrating progressive protection:

**Environment 1: Development**
- **Name**: `development`
- **Protection Rules**: None (auto-deploy)
- **Secrets**:
  - `DEV_API_ENDPOINT`
  - `DEV_DATABASE_URL`
- **Variables**:
  - `ENVIRONMENT_NAME`: development
  - `LOG_LEVEL`: debug
- **Use Case**: Automatic deployment on push to main/develop

**Environment 2: Staging**
- **Name**: `staging`
- **Protection Rules**:
  - Required reviewers: 1 reviewer from team
  - Wait timer: 5 minutes
  - Deployment branches: main, release/*
- **Secrets**:
  - `STAGING_API_ENDPOINT`
  - `STAGING_DATABASE_URL`
- **Variables**:
  - `ENVIRONMENT_NAME`: staging
  - `LOG_LEVEL`: info
- **Use Case**: Gated deployment with time delay

**Environment 3: Production**
- **Name**: `production`
- **Protection Rules**:
  - Required reviewers: 2 reviewers (different teams if possible)
  - Deployment branches: main only
  - Environment variables for approval bypass conditions
- **Secrets**:
  - `PROD_API_ENDPOINT`
  - `PROD_DATABASE_URL`
  - `PROD_SIGNING_KEY`
- **Variables**:
  - `ENVIRONMENT_NAME`: production
  - `LOG_LEVEL`: warn
- **Use Case**: Strict production deployment controls

**Environment Usage Workflow**:
- **File**: `.github/workflows/environment-demo.yml`
- Demonstrate deployment to all three environments
- Show environment-specific variable injection
- Demonstrate approval gates
- Show environment protection in action

### 6. Required Workflows in Organization Rulesets

Create documentation and example workflows for organization-level governance:

#### Documentation File
- **File**: `docs/REQUIRED_WORKFLOWS.md`
- **Content**:
  - Explanation of required workflows concept
  - How to configure organization rulesets
  - Step-by-step setup instructions
  - Best practices for required workflow design

#### Example Required Workflow 1: Security Baseline
- **File**: `.github/workflows/required-security.yml`
- **Purpose**: Mandatory security checks for all repositories
- **Features**:
  - Cannot be bypassed or disabled at repo level
  - Runs on all PRs and pushes
  - Blocks merge if critical vulnerabilities found
  - Required status check for branch protection
- **Checks**:
  - Secret scanning
  - Dependency vulnerability scan
  - SAST with CodeQL
  - License compliance check

#### Example Required Workflow 2: Compliance and Audit
- **File**: `.github/workflows/required-compliance.yml`
- **Purpose**: Enforce organizational compliance policies
- **Features**:
  - Verify commit signatures
  - Check for required files (LICENSE, SECURITY.md, CODE_OF_CONDUCT.md)
  - Validate PR descriptions meet template requirements
  - Enforce branch naming conventions
  - Audit trail logging

#### Ruleset Configuration Documentation
Include instructions for setting up rulesets that reference these workflows:
- Create organization-level ruleset
- Target repositories pattern (e.g., all repos, specific patterns)
- Reference required workflow repository
- Configure enforcement level (active vs. evaluate)

### 7. Marketplace Actions Restriction Policies

Create comprehensive documentation and examples:

#### Documentation File
- **File**: `docs/MARKETPLACE_RESTRICTIONS.md`
- **Content**:
  - Overview of GitHub Actions marketplace restrictions
  - Security implications of third-party actions
  - How to configure allowed actions policies
  - Organization vs. repository level policies
  - Versioning and update strategies

#### Example Allowed Actions Policy

**Policy Tiers to Demonstrate**:

1. **Allow All Actions** (Not Recommended)
   - Use case: Proof of concept, small teams
   - Risk profile: High

2. **Allow Verified Creators Only**
   - Use case: Balance between flexibility and security
   - Only GitHub-verified creators allowed
   - Example workflow showing usage

3. **Allow Specific Actions** (Recommended)
   - Use case: Enterprise security posture
   - Explicit allowlist approach
   - Example allowlist:
     ```
     actions/checkout@*
     actions/setup-node@*
     actions/setup-python@*
     actions/setup-java@*
     actions/setup-dotnet@*
     actions/cache@*
     actions/upload-artifact@*
     actions/download-artifact@*
     github/codeql-action/*
     docker/build-push-action@*
     azure/webapps-deploy@*
     ```

4. **Allow Local Actions Only**
   - Use case: Maximum security, air-gapped environments
   - Only actions within organization/repository
   - Example workflow using only local composite actions

#### Example Workflows Demonstrating Restrictions
- **File**: `.github/workflows/marketplace-policy-demo.yml`
- Create examples for each policy tier
- Document which actions would be blocked/allowed
- Show impact on workflow functionality
- Provide alternatives using composite actions

### 8. Additional Advanced Features to Include

#### Workflow Features
- **Matrix Strategy**: Demonstrate multi-dimensional matrices (OS × Language × Version)
- **Concurrency Control**: Prevent overlapping runs with concurrency groups
- **Workflow Dispatch**: Manual triggers with input parameters
- **Repository Dispatch**: External event triggering
- **Scheduled Workflows**: Cron-based execution for nightly builds
- **Workflow Status Badges**: README badges for build status
- **Job Dependencies**: Complex job orchestration with needs
- **Conditional Execution**: Advanced if conditions and expressions
- **Timeout Controls**: Job and step-level timeouts
- **Output Sharing**: Passing data between jobs and workflows

#### Security Best Practices
- **Least Privilege**: Minimal GITHUB_TOKEN permissions per job
- **Pin Actions to SHA**: Not tags/branches for supply chain security
- **Environment Variables**: Secure handling of sensitive data
- **OIDC Authentication**: Keyless cloud provider authentication demo (AWS/Azure)
- **Artifact Attestation**: Generate and verify build provenance

#### Observability and Debugging
- **Workflow Visualization**: Job dependency graphs
- **Debug Logging**: Enable debug mode examples
- **Annotations**: Create error/warning annotations
- **Job Summaries**: Generate markdown summaries in job output
- **PR Comments**: Automated PR commenting with results

### 9. Documentation Requirements

Create comprehensive documentation:

#### Main README.md
- Project overview and purpose
- Repository structure explanation
- Quick start guide for each technology stack
- Workflow architecture decision rationale
- Links to detailed documentation

#### docs/SETUP.md
- Prerequisites for running workflows
- Local development setup for each tech stack
- How to configure secrets and variables
- How to test workflows locally (act, nektos/act)
- Troubleshooting common issues

#### docs/WORKFLOWS.md
- Detailed explanation of each workflow
- Trigger conditions and path filters
- Input/output specifications
- Usage examples and screenshots
- Best practices per workflow pattern

#### docs/SECURITY.md
- Security considerations for GitHub Actions
- Secret management guidelines
- Third-party action vetting process
- Incident response for compromised workflows
- Regular security maintenance tasks

#### docs/ARCHITECTURE.md
- Architectural decision records (ADRs)
- Monolithic vs. separate workflow trade-offs
- Reusable workflow vs. composite action decision criteria
- Caching strategies and invalidation
- Artifact lifecycle management

### 10. Example Scenario Workflows

Create real-world scenario demonstrations:

#### Scenario 1: Pull Request Validation
- **File**: `.github/workflows/pr-validation.yml`
- Run on PR open/update
- All quality checks
- Size and complexity analysis
- Automated labeling
- Required status checks

#### Scenario 2: Release Process
- **File**: `.github/workflows/release.yml`
- Triggered by tag creation (v*.*.*)
- Build all applications
- Run full test suites
- Create GitHub Release
- Upload release artifacts
- Generate changelog
- Deploy to staging environment

#### Scenario 3: Dependency Update Automation
- **File**: `.github/workflows/dependency-update.yml`
- Scheduled weekly run
- Check for dependency updates
- Create PR with updates
- Run security scans on updated deps
- Auto-merge if tests pass (for patch updates)

#### Scenario 4: Performance Benchmarking
- **File**: `.github/workflows/performance-benchmark.yml`
- Scheduled nightly run
- Run performance tests for each app
- Compare against baseline
- Generate trend reports
- Alert on degradation

### 11. Testing and Validation

Include testing strategies for workflows:

#### Local Workflow Testing
- Instructions for using `act` (nektos/act)
- Local testing limitations
- Mock secret injection for local runs

#### Workflow Unit Tests
- Demonstrate workflow linting (actionlint)
- YAML validation
- Schema validation for custom actions

#### Integration Testing
- Test workflow files before merging
- Validate reusable workflow contracts
- End-to-end scenario testing

### Implementation Instructions

**Phase 1: Foundation**
1. Create repository structure with all app directories
2. Initialize each application with basic code
3. Create basic CI workflow for each stack
4. Set up caching for each package manager

**Phase 2: Reusable Components**
5. Develop composite actions
6. Create reusable workflows
7. Refactor stack-specific workflows to use reusable components
8. Create monolithic multi-stack workflow

**Phase 3: Security and Governance**
9. Implement security scanning workflows
10. Document required workflow setup
11. Create marketplace restriction documentation
12. Add OIDC authentication examples

**Phase 4: Environments and Secrets**
13. Create environment-based deployment workflow
14. Document secret configuration
15. Document variable usage patterns
16. Add environment protection examples

**Phase 5: Documentation and Polish**
17. Write comprehensive README
18. Create all documentation files
19. Add workflow status badges
20. Create architecture diagrams
21. Add usage examples and screenshots

### Success Criteria

The demo is complete when:
- ✅ Python technology stacks have working applications with tests
- ✅ Workflow patterns are implemented
- ✅ At least 3 reusable workflows are functional
- ✅ At least 3 composite actions are created
- ✅ Environment-based deployments work with protection rules
- ✅ Secrets and variables are documented with examples
- ✅ Required workflow concept is thoroughly documented
- ✅ Marketplace restrictions are explained with multiple policy examples
- ✅ All workflows execute successfully
- ✅ Documentation is comprehensive and includes diagrams
- ✅ Repository is ready for presentation and educational use

### Notes for Implementation
- Focus on demonstrating GitHub Actions features, not application complexity
- Use comments extensively in workflow files to explain concepts
- Ensure workflows can run in a forked repository with minimal setup
- Consider creating a "getting started" branch with partial implementation for learning
- Include links to GitHub documentation for each feature demonstrated
- Make workflows visually clear with descriptive job/step names
- Use consistent naming conventions across all workflows
