@_default:
    just --list

@bootstrap:
    python -m pip install --upgrade pip uv
    just sync

@build:
    uv build

@bump *ARGS:
    uv tool run bumpver update --allow-dirty {{ ARGS }}

@demo:
    uv run files-to-claude-xml.py \
        files-to-claude-xml.py \
        README.md

@fmt:
    just --fmt --unstable

@lint:
    uv run --with pre-commit-uv pre-commit run --all-files

@lock:
    uv lock

@publish:
    uv publish

@sync:
    uv sync
