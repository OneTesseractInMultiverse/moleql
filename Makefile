.PHONY: help pre-commit

install-pre-commit:
	uv add --dev pre-commit ruff

install-git-hook:
	uv run pre-commit install

pre-commit:
	uv run pre-commit run --all-files

test:
	uv run pytest -v
