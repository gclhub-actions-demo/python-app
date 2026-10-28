#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

app_dir="apps/python-service"
required_paths=(
  "$app_dir/app"
  "$app_dir/tests"
  "$app_dir/requirements.txt"
  "$app_dir/setup.py"
  "$app_dir/pytest.ini"
)

for path in "${required_paths[@]}"; do
  if [[ ! -e "$path" ]]; then
    echo "::error title=Python project layout::Required path is missing: $path"
    exit 1
  fi
done

if ! find "$app_dir/tests" -maxdepth 1 -type f -name 'test_*.py' -print -quit | grep -q .; then
  echo "::error title=Python project layout::No test_*.py files found in $app_dir/tests"
  exit 1
fi

echo "Python project layout is ready for the required CI checks."
