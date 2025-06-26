# Hanzo REPL

An intimate REPL environment for testing Hanzo's Model Context Protocol (MCP) tools and AI integration. Think of it as `rlwrap` meets Claude Code - direct access to MCP tools with IPython magic.

## Features

- 🎯 **Direct MCP Access**: All MCP tools available as Python functions
- 💬 **Integrated Chat**: Chat with AI that can use MCP tools
- 🔧 **IPython Magic**: Use `?` and `!` helpers, tab completion
- 🔄 **Live Editing**: Edit the REPL source code on the fly
- 🧪 **Built-in Tests**: Comprehensive test suite for MCP tools
- 🎨 **Rich Output**: Beautiful formatting with Rich library

## Quick Start

```bash
# Setup (one time)
make setup

# Start the REPL
make dev
```

## Usage Examples

### Direct Tool Access

```python
# All MCP tools are available as functions
>>> read_file(file_path="/etc/hosts")
>>> write_file(file_path="test.txt", content="Hello, World!")
>>> search(query="def main", path=".")
>>> run_command(command="ls -la")
```

### Chat with AI

```python
# Simple chat
>>> chat("What files are in the current directory?")

# AI will use MCP tools to answer
>>> chat("Create a Python script that prints the current time")

# Complex workflows
>>> chat("Find all Python files with 'test' in the name and show their sizes")
```

### IPython Magic Commands

```python
# Single-line chat
%chat What is the weather today?

# Multi-line chat
%%ai
Can you help me create a web scraper?
I need it to extract titles from a list of URLs.

# List available tools
%tools

# Execute specific tool
%tool read_file {"file_path": "README.md"}

# Edit REPL source
%edit_self ipython_repl.py

# Change model
%model claude-3-opus-20240229
```

### Object Access

```python
# Access MCP server directly
>>> mcp.tools.keys()

# Access LLM client
>>> llm.get_available_providers()
>>> llm.set_model("gpt-4")

# Access tool executor
>>> executor.get_context()
```

## Available Commands

### Makefile Targets

- `make dev` - Start IPython REPL with MCP tools
- `make test` - Run test suite
- `make demo-file` - Demo file operations
- `make demo-chat` - Demo chat functionality
- `make demo-search` - Demo search operations
- `make clean` - Clean generated files

### REPL Commands

- `chat(message)` - Chat with AI using MCP tools
- `tools.<tab>` - Tab completion for all tools
- `%tools` - List all available MCP tools
- `%model` - Show/set current LLM model
- `%edit_self` - Edit REPL source code

## Environment Variables

Set at least one LLM provider API key:

- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic/Claude API key
- `GROQ_API_KEY` - Groq API key
- Other providers supported by litellm

## Integration with Hanzo Chat

The REPL can be used as an MCP server for Hanzo Chat:

1. Start the REPL: `make dev`
2. Configure Hanzo Chat to use the MCP endpoint
3. All tools become available in the chat interface

## Testing

```bash
# Run all tests
make test

# Run integration tests (requires API keys)
make test-integration

# Interactive test in REPL
make test-repl
```

## Development

```bash
# Watch for changes and auto-restart
make watch

# Format code
make format

# Lint code
make lint

# Type check
make type-check
```

## Architecture

```
hanzo_repl/
├── ipython_repl.py    # IPython-based REPL with magic commands
├── llm_client.py      # Multi-provider LLM client
├── tool_executor.py   # Execute tools based on LLM responses
├── tests.py          # Comprehensive test suite
└── cli.py            # Command-line interface

mcp_repl.py           # Minimal direct-access REPL
```

## Why This Exists

This REPL provides a more intimate way to interact with Hanzo's MCP tools:

- No barriers between you and the tools
- Direct Python access to all functionality
- Chat with AI that can modify its own code
- Perfect for testing and development
- Great for learning the MCP API

Think of it as your personal MCP playground where you can experiment, test, and build with immediate feedback.