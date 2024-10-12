@_default:
    just --list

@bootstrap:
    python -m pip install --upgrade pip uv
    just sync

@build:
    uv build

@demo:
    uv run files-to-claude-xml.py \
        files-to-claude-xml.py \
        README.md

@fmt:
    just --fmt --unstable

@lint:
    uv run --with pre-commit-uv pre-commit run --all-files

@publish:
    uv publish

@sync:
    uv sync
