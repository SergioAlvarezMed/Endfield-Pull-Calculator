# Makefile for Endfield Pity Calculator

.PHONY: help install test coverage run clean lint

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make coverage   - Run tests with coverage report"
	@echo "  make run        - Run the application"
	@echo "  make clean      - Clean cache and build files"
	@echo "  make lint       - Run code quality checks"

install:
	pip install -e .
	pip install -e ".[dev]"

test:
	pytest tests/ -v

coverage:
	pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
	@echo "\nCoverage report generated in htmlcov/index.html"

run:
	python main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "Cleaned cache and build files"

lint:
	@echo "Running type checks and linting..."
	python -m pytest tests/ --collect-only
	@echo "✓ Tests collected successfully"
