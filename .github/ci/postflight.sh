#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

setup_file="apps/python-service/setup.py"

if ! grep -Fq 'name="python-microservice"' "$setup_file"; then
  echo "::error title=Python package metadata::Expected package name is missing from $setup_file"
  exit 1
fi

if ! grep -Fq 'python_requires=">=3.11"' "$setup_file"; then
  echo "::error title=Python package metadata::Python 3.11 minimum is missing from $setup_file"
  exit 1
fi

if ! grep -Fq 'Programming Language :: Python :: 3.11' "$setup_file"; then
  echo "::error title=Python package metadata::Python 3.11 classifier is missing from $setup_file"
  exit 1
fi

echo "Python package metadata matches the supported runtime."
