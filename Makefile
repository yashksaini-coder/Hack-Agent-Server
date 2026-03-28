.PHONY: lint format typecheck quality run help

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  lint      Run ruff check"
	@echo "  format    Run ruff format"
	@echo "  typecheck Run mypy"
	@echo "  quality   Run lint, format (check), and typecheck"
	@echo "  run       Run the application"

lint:
	uv run ruff check . --fix

check-lint:
	uv run ruff check .

format:
	uv run ruff format .

check-format:
	uv run ruff format . --check

typecheck:
	uv run mypy . --ignore-missing-imports

ci: check-lint check-format typecheck

run:
	uv run uvicorn app:app --host 0.0.0.0 --port 8000 --reload
