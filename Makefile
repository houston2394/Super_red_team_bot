.PHONY: help install test clean run lint

help:
	@echo "Super_red_team_bot - Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make test      - Run all tests"
	@echo "  make clean     - Clean up cache files"
	@echo "  make run       - Run the bot"
	@echo "  make lint      - Run linting"

install:
	pip install -r requirements.txt

test:
	python3 -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache

run:
	python3 bot.py --list-plugins

lint:
	@echo "Linting not configured - add your linter here"
