.PHONY: help setup install dev test lint format clean repl ipython chat

# Colors
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m

help: ## Show this help
	@echo "$(BLUE)Hanzo REPL$(NC)"
	@echo ""
	@echo "$(GREEN)Usage:$(NC)"
	@echo "  make $(YELLOW)[target]$(NC)"
	@echo ""
	@echo "$(GREEN)Main targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

setup: install-python ## Initial setup with Python and dependencies
	@echo "$(BLUE)Setting up Hanzo REPL...$(NC)"
	@if ! command -v uv &> /dev/null; then \
		echo "$(RED)Error: uv not found. Please install uv first.$(NC)"; \
		exit 1; \
	fi
	uv venv
	uv pip install -e .
	@echo "$(GREEN)Setup complete!$(NC)"

install-python: ## Install Python using uv
	@echo "$(BLUE)Installing Python...$(NC)"
	@if ! command -v uv &> /dev/null; then \
		echo "$(RED)Error: uv not found. Please install uv first.$(NC)"; \
		echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	fi
	uv python install 3.11
	@echo "$(GREEN)Python installed!$(NC)"

install: setup ## Install the REPL (alias for setup)

dev: ## Start IPython REPL with MCP tools
	@echo "$(BLUE)Starting Hanzo MCP REPL...$(NC)"
	@if [ ! -d ".venv" ]; then \
		echo "$(YELLOW)Virtual environment not found. Running setup...$(NC)"; \
		$(MAKE) setup; \
	fi
	@if [ -z "$$OPENAI_API_KEY" ] && [ -z "$$ANTHROPIC_API_KEY" ] && [ -z "$$GROQ_API_KEY" ]; then \
		echo "$(YELLOW)Warning: No API keys detected!$(NC)"; \
		echo "Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or another provider key"; \
		echo ""; \
	fi
	uv run python mcp_repl.py

repl: dev ## Start the REPL (alias for dev)

ipython: ## Start IPython-based REPL with magic commands
	@echo "$(BLUE)Starting IPython REPL...$(NC)"
	@if [ ! -d ".venv" ]; then \
		$(MAKE) setup; \
	fi
	uv run hanzo-repl

chat: ## Start basic chat interface
	@echo "$(BLUE)Starting chat interface...$(NC)"
	@if [ ! -d ".venv" ]; then \
		$(MAKE) setup; \
	fi
	uv run hanzo-repl --mode basic

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	uv run pytest tests/ -v

test-integration: ## Run integration tests (requires API keys)
	@echo "$(BLUE)Running integration tests...$(NC)"
	@if [ -z "$$OPENAI_API_KEY" ] && [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "$(RED)Error: Integration tests require API keys$(NC)"; \
		exit 1; \
	fi
	uv run pytest tests/test_chat_integration.py -v

test-repl: ## Test REPL functionality interactively
	@echo "$(BLUE)Testing REPL functionality...$(NC)"
	@echo "from hanzo_repl.tests import run_tool_tests; import asyncio; asyncio.run(run_tool_tests(console, mcp, executor))" | uv run hanzo-repl

lint: ## Lint with ruff
	@echo "$(BLUE)Linting code...$(NC)"
	uv run ruff check .

format: ## Format with black and ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	uv run black .
	uv run ruff check --fix .

type-check: ## Type check with mypy
	@echo "$(BLUE)Type checking...$(NC)"
	uv run mypy hanzo_repl/

clean: ## Clean generated files
	@echo "$(BLUE)Cleaning...$(NC)"
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete

# Demo commands
demo-file: ## Demo file operations
	@echo "$(BLUE)Demo: File operations$(NC)"
	@echo "write_file(file_path='demo.txt', content='Hello, Hanzo!')" | uv run python -m hanzo_repl.ipython_repl

demo-chat: ## Demo chat functionality
	@echo "$(BLUE)Demo: Chat with AI$(NC)"
	@echo "chat('What files are in the current directory?')" | uv run python -m hanzo_repl.ipython_repl

demo-search: ## Demo search functionality
	@echo "$(BLUE)Demo: Search operations$(NC)"
	@echo "search(query='class', path='.')" | uv run python -m hanzo_repl.ipython_repl

# Development helpers
watch: ## Watch for changes and restart
	@echo "$(BLUE)Watching for changes...$(NC)"
	watchmedo auto-restart --pattern="*.py" --recursive -- uv run hanzo-repl

shell: ## Start a shell in the virtual environment
	@echo "$(BLUE)Starting shell...$(NC)"
	uv run bash

# Installation to user's system
install-global: ## Install globally using pipx
	@echo "$(BLUE)Installing globally...$(NC)"
	pipx install -e .

# Integration with Hanzo Chat
integrate-chat: ## Set up integration with Hanzo Chat
	@echo "$(BLUE)Setting up Hanzo Chat integration...$(NC)"
	@echo "To integrate with Hanzo Chat:"
	@echo "1. Start the MCP server: make dev"
	@echo "2. In Hanzo Chat, configure MCP endpoint to use this REPL"
	@echo "3. Tools will be available in the chat interface"

# PyPI publishing
build: clean ## Build distribution packages
	@echo "$(BLUE)Building distribution...$(NC)"
	cp pyproject.toml pyproject.toml.dev
	cp pyproject.toml.pypi pyproject.toml
	uv build
	cp pyproject.toml.dev pyproject.toml
	@echo "$(GREEN)Build complete!$(NC)"

publish: build ## Publish to PyPI
	@echo "$(BLUE)Publishing to PyPI...$(NC)"
	uv publish
	@echo "$(GREEN)Published!$(NC)"

publish-test: build ## Publish to TestPyPI
	@echo "$(BLUE)Publishing to TestPyPI...$(NC)"
	uv publish --index-url https://test.pypi.org/simple/
	@echo "$(GREEN)Published to TestPyPI!$(NC)"

# Default target
.DEFAULT_GOAL := help