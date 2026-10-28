# Organization-Required Workflows

This repository demonstrates local GitHub Actions patterns, while the actual
organization-required CI workflow is maintained centrally in
[`gclhub-actions-demo/required-workflows`](https://github.com/gclhub-actions-demo/required-workflows)
and enforced through an organization ruleset. Do not treat the repository-local
workflows named `required-security.yml` or `required-compliance.yml` as that gate.

## Central Python CI contract

The central workflow applies to pull requests targeting `main`, including
documentation-only changes. Its required Python project checks use Python 3.11,
run flake8 and pytest, enforce the application's configured minimum coverage of
80%, and build the package.

The application is registered in [`.github/app-ci.json`](../.github/app-ci.json):

```json
{
  "version": 1,
  "projects": [
    {
      "id": "python",
      "path": "apps/python-service"
    }
  ],
  "extensions": {
    "preflight": ".github/ci/preflight.sh",
    "postflight": ".github/ci/postflight.sh"
  }
}
```

The manifest identifies the Python project path and optional repository-relative
extension scripts. The required commands and thresholds are centrally defined;
the manifest does not configure or replace them.

## Extension scripts

The example scripts add narrow, app-specific checks:

- `.github/ci/preflight.sh` verifies the service layout and that test modules exist.
- `.github/ci/postflight.sh` verifies the package name and Python 3.11 metadata.

Each extension runs independently in a fresh hosted job. It must therefore inspect
only the checked-out repository and cannot rely on build outputs, reports, or other
files produced by the central workflow's required-check jobs. Extensions are
additive and must not require secrets or write permissions.

## Repository-local workflow examples

The following workflows are retained as educational examples. Their triggers and
results are managed by this repository, and they are not substitutes for the
organization ruleset's required workflow:

| Workflow | Demonstration |
|----------|---------------|
| `.github/workflows/required-security.yml` | Local security scanning examples |
| `.github/workflows/required-compliance.yml` | Local compliance and audit examples |

Other repository workflows, including `ci.yml`, release automation, and reusable
workflow examples, continue to serve their existing purposes. They are independent
of the organization-level required CI gate.
