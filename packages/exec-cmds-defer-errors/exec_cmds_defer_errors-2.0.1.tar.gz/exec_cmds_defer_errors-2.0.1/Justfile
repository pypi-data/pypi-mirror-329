set dotenv-load

set shell := [
  "bash",
  "-o", "errexit", "-o", "nounset", "-o", "pipefail",
  "-O", "extglob", "-O", "globstar", "-O", "nullglob",
  "-c"
]

# Init, fix, check, and test.
default: init fix check test

# Initialize environment.
init:
  # Create local-only directories.
  mkdir -p \
    .cache \
    .cache/mypy \
    .cache/pytest \
    .cache/ruff \
    .local \
    .tmp \
    .venv

  # Check tool availability.
  filter-pre-commit-hooks --version
  mdformat --version
  pre-commit --version
  shellcheck --version
  shfmt --version
  uv --version
  yamlfmt --version

  # Install pre-commit hooks.
  pre-commit install --install-hooks
  pre-commit install --install-hooks --hook-type commit-msg
  pre-commit install --install-hooks --hook-type post-checkout
  pre-commit install --install-hooks --hook-type post-merge

  # Initialize project with uv.
  uv sync --all-extras --dev

# Update dependencies.
update:
  # Try to update tools managed with Homebrew.
  ./scripts/update-pkgs-brew.bash just shellcheck shfmt uv yamlfmt

  # Try to update tools managed with uv.
  ./scripts/update-pkgs-uv.bash copier mdformat pre-commit

  # Update pre-commit repositories and hooks.
  pre-commit autoupdate

  # Update project deps managed with uv.
  uv sync --upgrade --all-extras --dev

# Run recipes that fix stuff.
fix:
  ./scripts/exec_cmds_defer_errors.py \
    "just fix--pre-commit" \
    "just fix--mdformat" \
    "just fix--shfmt" \
    "just fix--ruff"

# Run pre-commit hooks that fix stuff.
fix--pre-commit:
  ./scripts/run-pre-commit-fixes.bash

# Format Markdown files with mdformat.
fix--mdformat:
  mdformat **/*.md

# Format shell scripts with shfmt.
fix--shfmt:
  shfmt --list --write **/*.bash **/*.sh

# Fix Python files with Ruff.
fix--ruff:
  uv run --quiet ruff format
  uv run --quiet ruff check --fix-only

# Run recipes that check stuff.
check:
  ./scripts/exec_cmds_defer_errors.py \
    "just check--pre-commit" \
    "just check--shellcheck" \
    "just check--ruff" \
    "just check--mypy"

# Run pre-commit hooks that check stuff.
check--pre-commit:
  ./scripts/run-pre-commit-checks.bash

# Lint shell scripts with ShellCheck
check--shellcheck:
  shellcheck **/*.bash **/*.sh

# Lint Python files with Ruff.
check--ruff:
  uv run --quiet ruff check --no-fix

# Lint Python files with mypy.
check--mypy:
  uv run --quiet dmypy run --timeout 3600 src tests

# Test project with pytest
test:
  uv run --quiet pytest --cov --cov-report=term-missing:skip-covered

# Sync dependencies from project config to script inline metadata.
[group('misc')]
sync-script-metadata:
  ./scripts/sync-script-metadata.bash src/$SCRIPT_NAME/$SCRIPT_NAME.py
