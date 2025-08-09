# List available commands
@_default:
    just --list

# Set up development environment
@bootstrap:
    python -m pip install --upgrade pip uv
    just sync

# Build the Python package
@build:
    uv build

# Increment version (YYYY.MM.INC format)
@bump *ARGS:
    uv tool run bumpver update --allow-dirty {{ ARGS }}

# Run example conversion
@demo:
    uv run files-to-claude-xml.py \
        files-to-claude-xml.py \
        README.md

# Format this justfile
@fmt:
    just --fmt --unstable

# Run code quality checks
@lint:
    uv run --with pre-commit-uv pre-commit run --all-files

# Update dependency lock file
@lock:
    uv lock

# Publish package to PyPI
@publish:
    uv publish

# Install project dependencies
@sync:
    uv sync

# Upgrade all dependencies to latest
@upgrade:
    uv sync --refresh --upgrade
