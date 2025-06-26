#!/usr/bin/env python3
"""Minimal MCP REPL - Direct access to Hanzo MCP tools in IPython."""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from IPython import embed
    from IPython.terminal.embed import InteractiveShellEmbed
    from rich.console import Console
    from rich.markdown import Markdown
    
    from hanzo_mcp.server import HanzoMCPServer
    from hanzo_repl.llm_client import LLMClient
    from hanzo_repl.tool_executor import ToolExecutor
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: uv pip install -e .")
    sys.exit(1)


# Global instances
console = Console()
mcp = None
llm = None
executor = None


def chat(message: str) -> str:
    """Chat with AI using MCP tools."""
    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(executor.execute_with_tools(message))
    console.print(Markdown(response))
    return response


def init():
    """Initialize MCP and LLM."""
    global mcp, llm, executor
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Initialize MCP
    mcp = HanzoMCPServer()
    loop.run_until_complete(mcp.initialize())
    
    # Initialize LLM
    llm = LLMClient()
    if not llm.get_available_providers():
        console.print("[red]No API keys found![/red]")
        console.print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
        return False
    
    # Initialize executor
    executor = ToolExecutor(mcp, llm)
    
    # Create tool shortcuts
    for name, tool in mcp.tools.items():
        # Create sync wrapper
        def make_wrapper(t):
            def wrapper(**kwargs):
                return loop.run_until_complete(t.execute(**kwargs))
            wrapper.__name__ = t.name
            wrapper.__doc__ = t.description
            return wrapper
        
        globals()[name] = make_wrapper(tool)
    
    return True


if __name__ == "__main__":
    if not init():
        sys.exit(1)
    
    # Print banner
    console.print("[bold cyan]Hanzo REPL[/bold cyan]")
    console.print(f"Model: [green]{llm.current_model}[/green]")
    console.print("\nAvailable:")
    console.print("  • chat('message') - Chat with AI")
    console.print("  • All MCP tools as functions")
    console.print("  • mcp, llm, executor objects")
    console.print("")
    
    # Start IPython
    embed(colors="Linux")