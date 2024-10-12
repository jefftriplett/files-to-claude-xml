@_default:
    just --list

@bootstrap:
    python -m pip install --upgrade pip uv

@build:
    uv build

@demo:
    uv run files-to-claude-xml.py \
        files-to-claude-xml.py

@fmt:
    just --fmt --unstable

@lint:
    uv run --with pre-commit-uv pre-commit run --all-files
