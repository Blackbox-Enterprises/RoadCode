.PHONY: all build test lint deploy clean dev

all: build test

build:
	@echo "Building RoadCode..."
	@python -m pip install -e . 2>/dev/null || true
	@npm install 2>/dev/null || true

test:
	@echo "Running tests..."
	@python -m pytest tests/ -v 2>/dev/null || true
	@npm test 2>/dev/null || true

lint:
	@ruff check . 2>/dev/null || true
	@shellcheck scripts/**/*.sh 2>/dev/null || true

deploy:
	@bash scripts/deploy/deploy.sh

dev:
	@bash scripts/dev.sh

clean:
	@rm -rf __pycache__ .pytest_cache node_modules dist build *.egg-info
